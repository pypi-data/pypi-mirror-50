
cdef extern from "Automaton.h":
    cdef struct State:
        int* f
        bint final

    cdef struct Automaton:
        State* e  # states
        int n   # number of states
        int na  # number of letters
        int i  # initial state

    cdef struct Transition:
        int l  # label
        int e  # arrival state

    cdef struct NState:
        Transition* a
        int n
        bint final
        bint initial

    cdef struct NAutomaton:
        NState* e  # states
        int n   # number of states
        int na  # number of letters

    Automaton CopyAutomaton (Automaton a, int nalloc, int naalloc)

cdef extern from "automataC.h":

    cdef struct Dict:
        int* e
        int n
    cdef struct InvertDict:
        Dict* d
        int n

    bint DotExists()
    NAutomaton NewNAutomaton(int n, int na)
    void FreeNAutomaton(NAutomaton *a)
    Automaton NewAutomaton(int n, int na)
    void FreeAutomaton(Automaton *a)
    int hashAutomaton(Automaton a)
    NAutomaton CopyNAutomaton(NAutomaton a, int nalloc, int naalloc)
    Automaton PieceAutomaton(Automaton a, int *w, int n, int e)
    void initAutomaton(Automaton *a)
    void initNAutomaton(NAutomaton *a)
    void printAutomaton(Automaton a)
    void plotDot(const char *file, Automaton a, const char **labels, const char *graph_name, double sx, double sy, const char **vlabels, bint html, bint verb, bint run_dot)
    void NplotDot(const char *file, NAutomaton a, const char **labels, const char *graph_name, double sx, double sy, bint run_dot)
    Automaton Product(Automaton a1, Automaton a2, Dict d, bint verb)
    Automaton Determinize(Automaton a, Dict d, bint noempty, bint onlyfinals, bint nof, bint verb)
    Automaton DeterminizeN(NAutomaton a, bint sink, int verb)
    NAutomaton Concat(Automaton a, Automaton b, bint verb)
    NAutomaton CopyN(Automaton a, bint verb)
    void AddTransitionN(NAutomaton *a, int e, int f, int l)
    void AddPathN(NAutomaton *a, int e, int f, int *l, int len, bint verb)
    NAutomaton Proj(Automaton a, Dict d, bint verb)
    void ZeroComplete(Automaton *a, int l0, bint verb)
    Automaton ZeroComplete2(Automaton *a, int l0, bint sink_state, bint verb)
    Automaton ZeroInv(Automaton *a, int l0)
    Automaton prune_inf(Automaton a, bint verb)
    Automaton prune(Automaton a, bint verb)
    Automaton pruneI(Automaton a, bint verb)
    void AccCoAcc(Automaton *a, int *coa)
    void CoAcc(Automaton *a, int *coa)
    bint equalsAutomaton(Automaton a1, Automaton a2, bint verb)
    Dict NewDict(int n)
    void FreeDict(Dict *d)
    void printDict(Dict d)
    InvertDict NewInvertDict(int n)
    void FreeInvertDict(InvertDict id)
    void printInvertDict(InvertDict id)
    Automaton Duplicate(Automaton a, InvertDict id, int na2, bint verb)
    Automaton MirrorDet(Automaton a)
    NAutomaton Mirror(Automaton a)
    int StronglyConnectedComponents(Automaton a, int *res)
    Automaton SubAutomaton(Automaton a, Dict d, bint verb)
    Automaton Permut(Automaton a, int *l, int na, bint verb)
    void PermutOP(Automaton a, int *l, int na, bint verb)
    Automaton Minimise(Automaton a, bint verb)
    void DeleteVertexOP(Automaton* a, int e)
    Automaton DeleteVertex(Automaton a, int e)
    bint equalsLanguages(Automaton *a1, Automaton *a2, Dict a1toa2, bint minimized, bint pruned, bint verb)
    bint Intersect(Automaton a1, Automaton a2, bint verb)
    bint Included(Automaton a1, Automaton a2, bint pruned, bint verb)
    # bint intersectLanguage (Automaton *a1, Automaton *a2, Dict a1toa2, bint pruned, bint verb)
    bint emptyLanguage(Automaton a)
    void AddState(Automaton *a, bint final)
    bint IsCompleteAutomaton(Automaton a)
    bint CompleteAutomaton(Automaton *a)
    Automaton BiggerAlphabet(Automaton a, Dict d, int nna) #copy the automaton with a new bigger alphabet
    bint findWord(Automaton a, Dict *w, bint verb)
    bint shortestWord(Automaton a, Dict *w, int i, int f, bint verb)
    bint shortestWords(Automaton a, Dict *w, int i, bint verb)
    bint rec_word(Automaton a, Dict d)
    void Test()


cdef class DetAutomaton:
    cdef Automaton* a
    cdef list A    # alphabet
    #cdef dict dA  # dictionnary giving the index in A
    cdef list S    # states
    #cdef dict dS  # dictionnary giving the index in S
    # cdef set_a(self, Automaton a)

cdef class CAutomaton:
    cdef NAutomaton* a
    cdef list A
    cdef list S    # states

