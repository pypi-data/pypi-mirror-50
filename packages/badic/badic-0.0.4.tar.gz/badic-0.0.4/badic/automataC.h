#include <stdint.h>
//#include "Automaton.h"

typedef uint64_t uint64;
typedef unsigned int uint;


struct Dict
{
	int *e;
	int n;
};
typedef struct Dict Dict;

int DotExists (void);

int hashAutomaton (Automaton a);
int findWord (Automaton a, Dict *w, int verb); //return a word of the language of a
int rec_word (Automaton a, Dict d); //check that the word w is recognized by the automaton a
int shortestWord (Automaton a, Dict *w, int i, int f, int verb); //return a shortest word of the language of a
int shortestWords (Automaton a, Dict *w, int i, int verb); //return shortest words toward each state
Dict NewDict (int n);
void FreeDict (Dict *d);
void printDict (Dict d);
void dictAdd (Dict *d, int e); //add the element to the disctionnary (even if already present)
Automaton NewAutomaton (int n, int na);
NAutomaton NewNAutomaton(int n, int na);
void ReallocNAutomaton (NAutomaton *a, int n);
void FreeAutomaton (Automaton *a);
void FreeAutomatons (Automaton* a, int n);
void FreeNAutomaton (NAutomaton *a);
void AddTransitionN (NAutomaton *a, int e, int f, int l);
void AddPathN (NAutomaton *a, int e, int f, int *l, int len, int verb);
NAutomaton CopyNAutomaton(NAutomaton a, int nalloc, int naalloc);
Automaton PieceAutomaton (Automaton a, int *w, int n, int e); //gives an automaton recognizing w(w^(-1)L) where L is the language of a starting from e
void initAutomaton (Automaton *a);
void initNAutomaton (NAutomaton *a);
void printAutomaton (Automaton a);
void plotDot (const char *file, Automaton a, const char **labels, const char *graph_name, double sx, double sy, const char **vlabels, int html, int verb, int run_dot);
void NplotDot (const char *file, NAutomaton a, const char **labels, const char *graph_name, double sx, double sy, int run_dot);
int equalsAutomaton (Automaton a1, Automaton a2, int verb); //determine if automata are the same (differents if permuted states)
int contract (int i1, int i2, int n1);
int geti1 (int c, int n1);
int geti2 (int c, int n1);
Automaton Product (Automaton a1, Automaton a2, Dict d, int verb);
Automaton Product2 (Automaton a1, Automaton a2, Dict d, int verb); //same without induction
void AddState(Automaton *a, int final);

struct States
{
	int *e;
	int n;	
};
typedef struct States States;

States NewStates (int n);
void FreeStates (States e);
void initStates (States e);
void printStates (States e);
int equals (States e1, States e2);
States copyStates (States e);

struct ListStates
{
	States *e;
	int n;
};
typedef struct ListStates ListStates;

void printListStates (ListStates l);
int AddEl (ListStates *l, States e, int* res); //add an element if not already in the list
void AddEl2 (ListStates *l, States e); //add an element even if already in the list

////////////////
struct States2
{
	uint n;
	uint64 *e;
};
typedef struct States2 States2;

States2 NewStates2 (int n);
void FreeStates2 (States2 e);
void initStates2 (States2 e);
void printStates2 (States2 e);
int isNullStates2 (States2 e);
int equalsStates2 (States2 e1, States2 e2);
int hasStates2 (States2 e, uint64 i);
States2 copyStates2 (States2 e);
void addState (States2 *e, uint64 i);

struct ListStates2
{
	States2 *e;
	int n; //number of states
	int na; //memory allocated
};
typedef struct ListStates2 ListStates2;

ListStates2 NewListStates2(int n, int na);
void ReallocListStates2(ListStates2* l, int n, int marge);
void FreeListStates2 (ListStates2* l);
void printListStates2 (ListStates2 l);

//inverse of a dictionnary
struct InvertDict
{
	Dict *d;
	int n;
};
typedef struct InvertDict InvertDict;

InvertDict NewInvertDict (int n);
InvertDict invertDict (Dict d);
void FreeInvertDict (InvertDict id);
void printInvertDict (InvertDict id);
void putState (States *f, int ef); /////////////to improve !!!!
void Determinize_ind (Automaton a, InvertDict id, Automaton* r, ListStates* l, int onlyfinals, int nof, int niter);
Automaton Determinize (Automaton a, Dict d, int noempty, int onlyfinals, int nof, int verb);
Automaton Determinize2 (Automaton a, Dict d, int noempty, int onlyfinals, int nof, int verb); //same without induction
NAutomaton Concat (Automaton a, Automaton b, int verb);
NAutomaton CopyN (Automaton a, int verb);
NAutomaton Proj (Automaton a, Dict d, int verb);

Automaton DeterminizeN (NAutomaton a, int puits, int verb);

//change the alphabet, duplicating edges if necessary
//the result is assumed deterministic !!!!
Automaton Duplicate (Automaton a, InvertDict id, int na2, int verb);

//add all the words that are in the language if we remove some ending zeroes
//zero is the letter of the alphabet of index l0
//i.e. the result has the language L(l0*)^(-1), if L is the language of a
void ZeroComplete (Automaton *a, int l0, int verb);
void ZeroComplete_ (Automaton *a, int l0, int verb); //same without induction

//add all the words that can be completed to a word of the language by adding some ending zeroes
//zero is the letter of index l0
//i.e. the result has the language L(l0*), if L is tha language of a
Automaton ZeroComplete2 (Automaton *a, int l0, int State_puits, int verb);

//Compute an automaton recognizing the language (l0*)L, where L is the language of a
Automaton ZeroInv (Automaton *a, int l0);

//retire tous les états à partir desquels il n'y a pas de chemin infini
Automaton prune_inf (Automaton a, int verb);

//Compute the mirror, assuming it is deterministic
Automaton MirrorDet (Automaton a);

//Compute the mirror
NAutomaton Mirror (Automaton a);

//Tarjan algorithm
int StronglyConnectedComponents (Automaton a, int *res);
int StronglyConnectedComponents2 (Automaton a, int *res); //same without induction

//determine accessible and co-accessible states
void AccCoAcc (Automaton *a, int *coa);

//determine co-accessible states
void CoAcc (Automaton *a, int *coa);

//retire tous les états non accessible ou non co-accessible
Automaton prune (Automaton a, int verb);

//retire tous les états non accessible
Automaton pruneI (Automaton a, int verb);

Automaton SubAutomaton (Automaton a, Dict d, int verb);

//permute les labels des arêtes
//l donne les anciens indices à partir des nouveaux
Automaton Permut (Automaton a, int *l, int na, int verb);
//idem mais SUR PLACE
void PermutOP (Automaton a, int *l, int na, int verb);

//minimisation par l'algo d'Hopcroft
//voir "Around Hopcroft’s Algorithm" de Manuel BACLET and Claire PAGETTI
Automaton Minimise(Automaton a, int verb);

void DeleteVertexOP(Automaton *a, int e);
Automaton DeleteVertex(Automaton a, int e);

//détermine si les langages des automates sont les mêmes
//le dictionnaires donne les lettres de a2 en fonction de celles de a1 (-1 si la lettre de a1 ne correspond à aucune lettre de a2). Ce dictionnaire est supposé inversible.
//if minimized is 1, the automaton a1 and a2 are assumed to be minimal.
int equalsLanguages (Automaton *a1, Automaton *a2, Dict a1toa2, int minimized, int pruned, int verb);
int equalsLanguages2 (Automaton *a1, Automaton *a2, Dict a1toa2, int minimized, int pruned, int verb); //same without induction

//détermine si le langage de l'automate a1 est inclus dans celui de a2
//le dictionnaires donne les lettres de a2 en fonction de celles de a1 (-1 si la lettre de a1 ne correspond à aucune lettre de a2). Ce dictionnaire est supposé inversible.
//if pruned is 1, the automaton a1 and a2 are assumed to be pruned.


//détermine si les langages des automates ont une intersection non vide
//le dictionnaires donne les lettres de a2 en fonction de celles de a1 (-1 si la lettre de a1 ne correspond à aucune lettre de a2). Ce dictionnaire est supposé inversible.
//if pruned is 1, the automaton a1 and a2 are assumed to be pruned otherwise it prunes.
//int intersectLanguage (Automaton *a1, Automaton *a2, Dict a1toa2, int pruned, int verb);

//détermine si l'intersection est vide ou non
int Intersect (Automaton a1, Automaton a2, int verb);
int Intersect2 (Automaton a1, Automaton a2, int verb); //same without induction

//détermine si l'on a inclusion des langages
int Included (Automaton a1, Automaton a2, int pruned, int verb);
int Included2 (Automaton a1, Automaton a2, int pruned, int verb); //same without induction

//détermine si le langage de l'automate est vide
int emptyLanguage (Automaton a);
int emptyLanguage2 (Automaton a); //same without induction

//determine if the automaton is complete (i.e. with his hole state)
int IsCompleteAutomaton (Automaton a);

//complete the automaton (i.e. add a hole state if necessary)
int CompleteAutomaton (Automaton *a);

//copy the automaton with a new bigger alphabet
Automaton BiggerAlphabet (Automaton a, Dict d, int nna);


