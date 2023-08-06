
struct State
{
	int *f; //list of na sons
	int final;
};
typedef struct State State;

struct Automaton
{
	State *e; //states
	int n; //number of states
	int na; //number of letters
	int i; //initial state
	//
//	int nalloc; //internal usage, allocated memory
};
typedef struct Automaton Automaton;

//Automaton NewAutomaton (int n, int na);
//void FreeAutomaton (Automaton *a);

///////////////////////////////////////////////////////
//Non Deterministaic Automata
///////////////////////////////////////////////////////

struct Transition
{
	int l; //label (-1 : epsilon-transition)
	int e; //arrival state
};
typedef struct Transition Transition;

struct NState
{
	Transition *a;
	int n;
	int final;
	int initial;
};
typedef struct NState NState;

struct NAutomaton
{
	NState *e; //states
	int n; //number of states
	int na; //number of letters
};
typedef struct NAutomaton NAutomaton;

Automaton CopyAutomaton (Automaton a, int nalloc, int naalloc);

