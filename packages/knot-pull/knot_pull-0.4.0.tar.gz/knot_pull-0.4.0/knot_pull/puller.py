from __future__ import print_function
from numpy import array as Vector
from collections import namedtuple

from .vector_ops import *
from .kpclasses import Bead,chainDeepCopy
from .writer import *
from .reader import *
from .config import EPSILON,VERBOSE
from knot_pull.finder import find_frame


def too_far(p1 ,p2 ,p3 ,i0 ,i1):
    """Checks if crossing is possible - 9 A from all triangle points is impossible due to single connection
    length restrictions"""
    return all([point_distance(p1 ,i0 )>=9. ,point_distance(p2 ,i0 ) >9. ,point_distance(p3 ,i0 ) >9.]) \
            or all([point_distance(p1 ,i1 )>=9. ,point_distance(p2 ,i1 ) >9. ,point_distance(p3 ,i1 ) >9.])


def inspectingOtherLines(p1, p2, p3, i0, i1, greedy=0, log=0):
    """Looks for connections going through the triangle. Starts with second connection from each triangle end"""

    potentials = []
    potids = []

    p123normal = get_normal(p1, p2, p3)

    inspected = i0
    if inspected and not inspected.Nhand:
        if found_crossing(p1,p2,p3, inspected.vec, l1=None, p123normal=None):
            potentials.append(inspected.vec)

    while inspected and inspected.Nhand:
        if inspected.Nhand.end:#Skip "Virtual" connection - between chain ends
            inspected = inspected.Nhand
            continue
        l0, l1 = inspected.vec, inspected.Nhand.vec

        #greedy can have distances larger than allowed in too_far()
        i = False if (greedy == 0 and too_far(p1, p2, p3, l0, l1)) else found_crossing(p1, p2, p3, l0, l1, p123normal)

        if i is not False:
            potentials.append(i)
        inspected = inspected.Nhand

    inspected = i1
    if inspected and not inspected.Chand:
        if found_crossing(p1,p2,p3, inspected.vec, l1=None, p123normal=None):
            potentials.append(inspected.vec)
    while inspected and inspected.Chand:
        if inspected.end:
            inspected = inspected.Chand
            continue
        l0, l1 = inspected.vec, inspected.Chand.vec

        #greedy can have distances larger than allowed in too_far()
        i = False if (greedy == 0 and too_far(p1, p2, p3, l0, l1)) else found_crossing(p1, p2, p3, l0, l1, p123normal)
        if i is not False:
            potentials.append(i)
        inspected = inspected.Chand
    return potentials

def filter_greedy(atoms, outfile='', len_frames=0):
    """Removes all superfluous atoms(kept for PyMOL purposes, to better detect topology"""
    current = atoms[0]
    latom = 0 #num of removed atoms
    changed = False
    while current.Chand and current.Chand.Chand:
        if current.Chand.end: #Skips "virtual" connections at chain ends
            current = current.Chand.Chand
            continue
        if current.end:
            current = current.Chand
            continue

        i0 = current.Nhand
        i1 = current.Chand.Chand.Chand if current.Chand and current.Chand.Chand else False

        potentials = inspectingOtherLines(current.vec, current.Chand.vec, current.Chand.Chand.vec, i0, i1, greedy=True)

        if potentials:
            current = current.Chand
            continue
        else:
            changed = changed or (not current.Chand.recent)
            current.setChand(current.Chand.Chand)
            current.Chand.setNhand(current)

            latom += 1
            continue
            ## TODO specjalnie nie zamieniam current - watpliwe, ale a noz widelec jeszcze jeden?

    while current.Chand: #renumbering needs to start from the C terminus
        current = current.Chand

    atoms = []
    while current:
        current.recent = max(0, current.recent - 1)
        atoms.append(current)
        current = current.Nhand
    atoms.reverse()

    for i, at in enumerate(atoms):
        at.setId(i)

    return atoms, changed


def prefilter_with_adding(atoms):
    """Removes atoms to reduce the backbone where possible. Adding new joints to long connections
    allows for reducing bumps"""

    current = atoms[0]

    #print(list((x.id,x.original_id) for x in atoms))

    latom = 0
    changed = False
    while current.Chand and current.Chand.Chand:
        if current.Chand.end: #skip "Virtual" connections at chain ends
            current = current.Chand.Chand
            continue
        if current.end:
            current = current.Chand
            continue

        i0 = current.Nhand
        i1 = current.Chand.Chand.Chand if current.Chand and current.Chand.Chand else False

        potentials = inspectingOtherLines(current.vec, current.Chand.vec, current.Chand.Chand.vec, i0, i1)

        if potentials:
            if point_distance(current.vec, current.Chand.vec) > 3.:
                #adds new joints to all "long " conections when can't reduce, maybe will go over the problem

                new_N = get_middlepoint(current.vec, current.Chand.vec)

                nowy_id = (current.original_id + current.Chand.original_id) / 2.
                if int(nowy_id) != nowy_id:
                    if int(nowy_id) != current.original_id:
                        nowy_id = int(nowy_id)
                    else:
                        nowy_id = int(nowy_id) + 1

                nowy = Bead(Vector(new_N), "CA", nowy_id)
                nowy.recent = 2
                nowy.setId((current.id+current.Chand.id)/2.)
                #print("Added", nowy.id, nowy.original_id, "between", current.id, current.original_id, "and",
                #      current.Chand.id, current.Chand.original_id)
                nowy.setNhand(current)
                nowy.setChand(current.Chand)
                current.Chand.setNhand(nowy)
                current.setChand(nowy)
            current = current.Chand
            continue
        else:
            if point_distance(current.vec, current.Chand.Chand.vec) < 4.:  # TODO may be too far?
                #if can be remove, and the distance is not so great - remove the atom
                changed = changed or (not current.Chand.recent)
                #print("Removing currC", current.Chand)
                current.setChand(current.Chand.Chand)
                current.Chand.setNhand(current)
                latom += 1
#                current = current.Chand
                continue
                ## TODO specjalnie nie zamieniam current - watpliwe, ale a noz widelec jeszcze jeden?
            else:
                position = get_middlepoint(current.vec, current.Chand.Chand.vec)
                # if we can reduce but the distance is too great - remove the atom, put a new one on the connection
                # reduces traingles to straight line

                changed = changed or point_distance(current.Chand.vec, position) > EPSILON

                nowy_id = (current.original_id + current.Chand.Chand.original_id) / 2.

                nowy = Bead(Vector(position), "CA", nowy_id)
                nowy.recent = 2
                nowy.setId(current.Chand.id) #replaces current atom
                #print("replaced", nowy.id, nowy.original_id, "between", current.id, current.original_id, "and",
                 #     current.Chand.Chand.id, current.Chand.Chand.original_id)
                nowy.setNhand(current)
                nowy.setChand(current.Chand.Chand)
                current.Chand.Chand.setNhand(nowy)
                current.setChand(nowy)
                current = current.Chand
                continue

    while current.Chand:
        current = current.Chand

    atoms = []
    while current:
        current.recent = max(0, current.recent - 1)
        atoms.append(current)
        current = current.Nhand
    atoms.reverse()

    for i, at in enumerate(atoms):
        at.setId(i)

    #print(list((x.id,x.original_id) for x in atoms))
    #exit()

    return atoms, changed

def run_through_filtering(atoms, config, greedy=0):
    """Governs reduction process and when it should end (when there is no improvement)"""

    frames = []
    frames.append([(x.original_id, x.vec, x.end) for x in atoms])
    o_and_t = config.get('outfile',0) and config.get('trajectory',0)

    if o_and_t:
        #print_out_last_pdb(config, frames, atoms)
        print_out_last_frame(config, atoms, len(frames))

    if not config or not config['no_pulling']:
        atoms, changed = prefilter_with_adding(atoms)

        frames_without_shortening = 0
        atoms_num = len(set(_.tuple() for _ in atoms))

        while changed:  # TODO should check RMSD up to 2 steps back
            frames.append([(x.original_id, list(x.vec), x.end) for x in atoms])
            if len(frames) >= 3 and len(frames[-1]) == len(frames[-3]):
                if all([all(i == j for i, j in zip(x[1], y[1])) for x, y in zip(frames[-1], frames[-3])]):
                    # if two frames back we had the exact same positions
                    break
                if len(set(_.tuple() for _ in atoms)) == atoms_num:
                    frames_without_shortening += 1
                else:
                    atoms_num = len(set(_.tuple() for _ in atoms))
                    frames_without_shortening = 0
                if frames_without_shortening > 2*len(atoms):
                    if VERBOSE: print ("Breaking filtering due to to not enough change")
                    break

            if o_and_t:
                #print_out_last_pdb(config, frames, atoms)
                print_out_last_frame(config, atoms, len(frames))

            atoms, changed = prefilter_with_adding(atoms)

        #    frames.append([(x.original_id, x.vec) for x in atoms])

    if VERBOSE:
        print ("Finished filtering, have {} atoms".format(len(atoms)))

    if greedy: #reduce number of atoms (improves topology detection)
        atoms, _ = filter_greedy(atoms, config, len(frames))
        frames.append([(x.original_id, x.vec, x.end) for x in atoms])
        if VERBOSE:
            print ("Finished greedy filtering, have {} atoms".format(len(atoms)))

    if o_and_t:
        #print_out_last_pdb(config, frames, atoms)
        print_out_last_frame(config, atoms, len(frames))

    return frames,atoms

def run_through_division(atoms):
    """Finds connections which can be safely cut (connected segments can't be simplified even separately) """
    if VERBOSE: print ("Starting with {} atoms".format(len(atoms)))
    cuts = []
    for i in range(1, len(atoms) - 2):  # No sense in checking last edges
        j = i + 1
        if VERBOSE: print("Cutting edge {}".format(j))
        _middle = get_middlepoint(atoms[i].vec, atoms[j].vec)
        _tmp1 = chainDeepCopy(atoms[:j] + [Bead(_middle, "CA")])
        _, _tmp1a = run_through_filtering(_tmp1, {}, greedy=1)
        if VERBOSE: print("Left from {} to {}".format(len(_tmp1),len(_tmp1a)))
        _tmp2 = chainDeepCopy([Bead(_middle, "CA")] + atoms[j:])  #
        _, _tmp2a = run_through_filtering(_tmp2, {}, greedy=1)
        if VERBOSE: print("Right from {} to {}".format(len(_tmp2),len(_tmp2a)))
        if _tmp1 == _tmp1a and _tmp2 == _tmp2a:  # no reduction
            # print i,
            cuts.append(i)

    cuts = [0] + cuts + [len(atoms) - 1]  # fix to get proper segment indices
    atom_lists = []
    if VERBOSE: print("Cuts: {}".format(cuts))

    for i in range(0, len(cuts) - 1):
        cutl = cuts[i]
        cutr = cuts[i + 1]
        lista = []
        if cutl:  # add middlepoints of our breakable edges
            _mid_l = get_middlepoint(atoms[cutl].vec, atoms[cutl + 1].vec)
            lista.append(Bead(_mid_l, "CA"))
        lista += atoms[cutl + bool(cutl):cutr + 1]
        if cutr < len(atoms) - 2:
            _mid_r = get_middlepoint(atoms[cutr].vec, atoms[cutr + 1].vec)
            lista.append(Bead(_mid_r, "CA"))
        lista = chainDeepCopy(lista)
        atom_lists.append(lista)

    return atom_lists  # returns all separateable segments


def pull(atoms, config, chain_names, get_representative=0,greedy=0):#, greedy_file="",trajectory=True,quiet=False, chain_names=(),rna=False):
    outfile = config['outfile']

    frames, atoms = run_through_filtering(atoms, config, greedy=greedy)
    quiet = config['quiet']
    repr = []
    if get_representative:
        Atom = namedtuple("Atom","original_id x y z end")
        repr = find_frame(frames)
        repr = [Atom(x[0],x[1][0],x[1][1],x[1][2],x[2]) for x in repr]

    chains = []
    model_num = len(frames)+1
    separate_chains = divide_into_bead_chains(atoms)
    for c, chain in enumerate(separate_chains):
        ch = Chain(c,chain)
        if chain_names: ch.setChainName(chain_names[c])
        if outfile:
            if not quiet: model_num = ch.print2file(config,model_num)
        chains.append(ch)

    for _,c1 in enumerate(chains):
        for c2 in chains[_+1:]:
            if are_chains_linked(c1,c2):
                c1.neighbours.append(c2)
                c2.neighbours.append(c1)

    return chains,repr

def same_vecs(l1,l2):
    return all(np.array_equal(x.vec,y.vec) for x,y in zip(l1,l2))

def are_chains_linked(ch1,ch2):
    _tmp_both = chainDeepCopy(ch1.atoms+ch2.atoms)
    _tmp_both[len(ch1.atoms)-1].end = True
    _tmp_ch1 = chainDeepCopy(ch1.atoms)
    _tmp_ch2 = chainDeepCopy(ch2.atoms)

    _,_both = run_through_filtering(_tmp_both, {}, greedy=1)
    _,_ch1 = run_through_filtering(_tmp_ch1, {}, greedy=1)
    _,_ch2 = run_through_filtering(_tmp_ch2, {}, greedy=1)
    return not same_vecs(_both,_ch1+_ch2)


class Chain:
    def __init__(self,chain,atoms):
        self.chain = chain
        self.atoms = atoms
        self.atom_lists = run_through_division(atoms)
        self.knots = []
        self.neighbours = []
        self.closing_path = closeTheCurve(atoms)
        self.closing_paths = [closeTheCurve(a) for a in self.atom_lists]
        self.wanda = None
        self.dowker = None
        self.dowker_code = None
        self.chain_name = ""


    def setChainName(self,c):
        self.chain_name = "({})".format(c)

    def print2file(self,config,model_num):
        #print_out_one_frame(outfile, self.atoms, model_num,self.chain)
        model_num+=1
        for alist in self.atom_lists:
            #print_out_one_frame(outfile, alist, model_num,self.chain,self.rna)
            print_out_last_frame(config, alist, model_num, cur_chain=self.chain_name[1:-1], final=True)
            model_num+=1
        return model_num



if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as input:
        atoms = input.readlines()
    if len(sys.argv) > 2:
        atoms = atoms[int(sys.argv[2]):int(sys.argv[3]) + 1]
    print ("Result is", run_through_filtering(atoms, sys.argv[1] + (
        "{}_{}".format(sys.argv[2], sys.argv[3]) if len(sys.argv) > 2 else "") + ".outall.pdb"))


