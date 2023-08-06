#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//#include <math.h>
#include "Automaton.h"
#include "automataC.h"

typedef Automaton Automaton;

static unsigned int log (unsigned int val)
{
    if (val == 0) return 0;
    if (val == 1) return 0;
    unsigned int ret = 0;
    while (val > 1) {
        val >>= 1;
        ret++;
    }
    return ret;
}

int min (int a, int b)
{
    if (a < b)
        return a;
    return b;
}

//test if the dot command is installed in the system
int DotExists ()
{
    int res = 1;
    system("command -v dot > testdot");
    FILE *f = fopen("testdot","r");
    fseek(f, 0, SEEK_END);
    if (ftell(f) == 0)
        res = 0;
    fclose(f);
    return res;
}

Dict NewDict(int n)
{
	Dict r;
	r.n = n;
	if (n == 0)
		return r;
	r.e = (int *)malloc(sizeof(int)*n);
	if (!r.e)
	{
		printf("Out of memory !\n");
		exit(15);
	}
	int i;
	for (i=0;i<n;i++)
	{
		r.e[i] = -1;
	}
	return r;
}

void FreeDict (Dict *d)
{
	if (d->n == 0)
		return;
	free(d->e);
	d->n = 0;
	d->e = NULL;
}

void printDict (Dict d)
{
	int i;
	printf("[ ");
	for (i=0;i<d.n;i++)
	{
		printf("%d ", d.e[i]);
	}
	printf("]\n");
}

//Add an element to the dictionnary (even if already in)
void dictAdd (Dict *d, int e)
{
	d->n++;
	if (d->n == 1)
		d->e = (int *)malloc(sizeof(int));
	else
		d->e = (int *)realloc(d->e, sizeof(int)*d->n);
	if (!d->e)
	{
		printf("Out of memory !");
		exit(1);
	}
	d->e[d->n-1] = e;
}

#define DISP_MEMORY	0

Automaton NewAutomaton(int n, int na)
{
#if DISP_MEMORY
	printf("New %d...\n", n);
#endif
	Automaton a;
	a.n = n;
	a.na = na;
	a.i = -1;
	if (n == 0)
	{
		a.e = NULL;
		return a;
	}
	a.e = (State *)malloc(sizeof(State)*n);

#if DISP_MEMORY
	printf("new aut %ld\n", a.e);
#endif
	
	//a.nalloc = n;
	if (!a.e)
	{
		printf("Out of memory !");
		exit(6);
	}
	int i,j;
	for (i=0;i<n;i++)
	{
		a.e[i].f = (int *)malloc(sizeof(int)*na);
		if (!a.e[i].f)
		{
			printf("Out of memory !");
			exit(7);
		}
		for (j=0;j<na;j++)
		{
			a.e[i].f[j] = -1;
		}
	}
	return a;
}

void FreeAutomaton(Automaton *a)
{
#if DISP_MEMORY
	printf("Free %d ...\n", a->n);
#endif
	//if (a.nalloc == 0 || a.n==0)
	if (a->n == 0 || a->e == NULL)
		return;
	int i;
	for (i=0;i<a->n;i++)
	{
		free(a->e[i].f);
	}
	//printf("free %ld\n", a->e);
	free(a->e);
	//a.nalloc = 0;
	a->n = 0;
}

void FreeAutomatons (Automaton* a, int n)
{
	int j;
	for (j=0;j<n;j++)
	{
		FreeAutomaton(&a[j]);
	}
}

int hashAutomaton (Automaton a)
{
	int h = 3;
	h += a.n + 1009*a.na + 1000003*a.i;
	int i, j;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			h += a.e[i].f[j];
			h = (h*1009) % 1000000007;
		}
		h += (a.e[i].final == 0);
		h = (h*1009) % 1000000007;
	}
	return h;
}

NAutomaton NewNAutomaton(int n, int na)
{
	NAutomaton a;
	a.n = n;
	a.na = na;
	if (n == 0)
	{
		a.e = NULL;
		return a;
	}
	a.e = (NState *)malloc(sizeof(NState)*n);
	if (!a.e)
	{
		printf("Out of memory !");
		exit(6);
	}
	int i;
	for (i=0;i<n;i++)
	{
		a.e[i].a = NULL;
		a.e[i].n = 0;
		a.e[i].final = 0;
		a.e[i].initial = 0;
	}
	return a;
}

void ReallocNAutomaton (NAutomaton *a, int n)
{
	if (a->n)
		a->e = (NState*)realloc(a->e, sizeof(NState)*n);
	else
		a->e = (NState*)malloc(sizeof(NState)*n);
	if (a->n < n)
	{
		int i;
		for (i=a->n;i<n;i++)
		{
			a->e[i].a = NULL;
			a->e[i].n = 0;
			a->e[i].initial = 0;
			a->e[i].final = 0;
		}
	}
	a->n = n;
}

void FreeNAutomaton(NAutomaton *a)
{
	if (a->n == 0)
		return;
	int i;
	for (i=0;i<a->n;i++)
	{
		if (a->e[i].n > 0)
		{
			free(a->e[i].a);
		}
	}
	free(a->e);
	a->n = 0;
}

//add an edge on the CAutomaton
void AddTransitionN (NAutomaton *a, int e, int f, int l)
{
	a->e[e].n++;
	if (a->e[e].n > 1)
		a->e[e].a = (Transition *)realloc(a->e[e].a, sizeof(Transition)*a->e[e].n);
	else
		a->e[e].a = (Transition *)malloc(sizeof(Transition));
	a->e[e].a[a->e[e].n - 1].e = f;
	a->e[e].a[a->e[e].n - 1].l = l;
}

//Add a path between states e and f of CAutomaton a
void AddPathN (NAutomaton *a, int e, int f, int *l, int len, int verb)
{
	int n = a->n;
	if (len > 1)
	{
		//Add new states
		if (verb)
			printf("realloc to size %d\n", a->n+len-1);
		ReallocNAutomaton(a, a->n+len-1);
		int i;
		AddTransitionN(a, 0, n, l[0]);
		for (i=1;i<len-1;i++)
		{
			if (verb)
				printf("add edge %d --%d--> %d\n", n+i-1, l[i], n+i);
			AddTransitionN(a, n+i-1, n+i, l[i]);
		}
		if (verb)
			printf("add edge %d --%d--> %d\n", n+len-2, l[len-1], f);
		AddTransitionN(a, n+len-2, f, l[len-1]);
	}else
	{
		if (len == 1)
		{
			AddTransitionN(a, e, f, l[0]);
		}
	}
}

void ReallocAutomaton (Automaton *a, int n, int init)
{
	if (a->n > n)
	{
		//free states to suppress
		int i;
		for (i=n;i<a->n;i++)
		{
			free(a->e[i].f);
		}
	}
	if (a->n)
		a->e = (State*)realloc(a->e, sizeof(State)*n);
	else
		a->e = (State*)malloc(sizeof(State)*n);
	if (a->n < n)
	{
		int i;
		for (i=a->n;i<n;i++)
		{
			a->e[i].f = (int *)malloc(sizeof(int)*a->na);
			if (init)
			{
				int j;
				for (j=0;j<a->na;j++)
				{
					a->e[i].f[j] = -1;
				}
			}
		}
	}
	a->n = n;
}

NAutomaton CopyNAutomaton(NAutomaton a, int nalloc, int naalloc)
{
    NAutomaton r = NewNAutomaton(nalloc, naalloc);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		r.e[i].final = a.e[i].final;
		r.e[i].initial = a.e[i].initial;
		r.e[i].a = (Transition*)malloc(sizeof(Transition)*a.e[i].n);
		r.e[i].n = a.e[i].n;
		for (j=0;j<a.e[i].n;j++)
		{
			r.e[i].a[j].l = a.e[i].a[j].l;
			r.e[i].a[j].e = a.e[i].a[j].e;
		}
	}
	return r;
}

Automaton CopyAutomaton(Automaton a, int nalloc, int naalloc)
{
	//a.n, a.na
	Automaton r = NewAutomaton(nalloc, naalloc);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		r.e[i].final = a.e[i].final;
		for (j=0;j<a.na;j++)
		{
			r.e[i].f[j] = a.e[i].f[j];
		}
	}
	r.i = a.i;
	return r;
}

//give an automaton recognizing w(w^(-1)L) where L is the language of a starting from state e
Automaton PieceAutomaton(Automaton a, int *w, int n, int e)
{
	int i, j, f;
	Automaton r = NewAutomaton(a.n+n, a.na);
	//put the states for the word w
	for (i=0;i<n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			r.e[i].f[j] = -1;
		}
		r.e[i].f[w[i]] = i+1;
		r.e[i].final = 0;
		f = a.e[e].f[w[i]];
		e = f;
	}
	if (n > 0)
		r.e[n-1].f[w[n-1]] = e+n;
	//test if empty
	if (n > 0 && f == -1)
	{
		FreeAutomaton(&r);
		return NewAutomaton(0, a.na);
	}
	//put the states of the automaton a
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] == -1)
				r.e[i+n].f[j] = -1;
			else
				r.e[i+n].f[j] = a.e[i].f[j]+n;
		}
		r.e[i+n].final = a.e[i].final;
	}
	if (n > 0)
		r.i = 0;
	else
		r.i = a.i;
	return r;
}

void initAutomaton (Automaton *a)
{
	int i,j;
	a->i = -1;
	for (i=0;i<a->n;i++)
	{
		a->e[i].final = 0;
		for (j=0;j<a->na;j++)
		{
			a->e[i].f[j] = -1;
		}
	}
}

void initNAutomaton (NAutomaton *a)
{
	int i;
	for (i=0;i<a->n;i++)
	{
		a->e[i].initial = 0;
		a->e[i].final = 0;
		a->e[i].a = NULL;
		a->e[i].n = 0;
	}
}

void printAutomaton(Automaton a)
{
	printf("Automaton with %d states, %d letters.\n", a.n, a.na);
	int i, j;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] != -1)
			{
				printf("%d --%d--> %d\n", i, j, a.e[i].f[j]);
			}
		}
	}
	printf("initial state %d.\n", a.i);
}

void plotDot (const char *file, Automaton a, const char **labels, const char *graph_name, double sx, double sy, const char **vlabels, int html, int verb, int run_dot)
{
	char tamp[1024];
	if (verb)
	    printf("Open file %s...", file);
	FILE *f = fopen(file, "w");
	if (!f)
	{
		printf("Unable to open file %s !\n", file);
		return;
	}
	
	if (verb)
		printf("start...\n");
	fprintf(f, "digraph %s\n{\n"\
	"	node[fontsize=20]"\
	"	edge[fontsize=20, arrowhead = open]"\
	"	rankdir = LR;\n"\
	"	size = \"%lf, %lf\";\n"\
	"	center = 1;\n"\
	"	nodesep = \"0.2\"\n", graph_name, sx, sy);
//	"	ranksep = \"0.4 equally\";\n", graph_name);
//	"	rotate = -90\n"\
//	"	orientation=landscape\n"\
//	"orientation = Landscape\n");
	if (verb)
		printf("write...\n");
	
	fprintf(f, "	\n");
	int i,j;
	for (i=0;i<a.n;i++)
	{
		fprintf(f, "	%d [shape=", i);
		if (a.e[i].final)
			fprintf(f, "doublecircle");
		else
			fprintf(f, "circle");
		fprintf(f, ", style=");
		if (i == a.i)
			fprintf(f, "bold");
		else
			fprintf(f, "solid");
		if (vlabels)
		{
			if (verb)
			{
				printf("ptz : i=%d : %s\n", i, vlabels[i]);
			}
			fprintf(f, ", label=%s", vlabels[i]);
		}
		fprintf(f, ", fontsize=20, margin=0]\n");
	}
	fprintf(f, "	\n");
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] != -1)
			{
			    const char *ptr = labels[j];
			    int dotted = 0;
			    if (labels[j][0] == '.' && labels[j][1] == '.' && labels[j][2] == '.')
			    {
			        ptr += 3;
			        dotted = 1;
				}
				if (html)
    				fprintf(f, "	%d -> %d [label=<%s>", i, a.e[i].f[j], ptr);
    			else
    			    fprintf(f, "	%d -> %d [label=\"%s\"", i, a.e[i].f[j], ptr);
    			if (dotted)
    			{
    			    fprintf(f, ", style=\"dotted\"");
    			}
    			fprintf(f, "]\n");
			}
		}
	}
	fprintf(f, "}\n");
	
	fclose(f);
	if (run_dot)
	{
        if (verb)
            printf("draw...\n");
        sprintf(tamp, "dot %s -Gname -Tpng > %s.png", file, file);
        system(tamp);
	}
}

void NplotDot (const char *file, NAutomaton a, const char **labels, const char *graph_name, double sx, double sy, int run_dot)
{
	int verb = 0;
	char tamp[1024];
	//FILE *f = fopen(temp_dot_file_name, "w");
	FILE *f = fopen(file, "w");
	if (!f)
	{
		printf("Unable to open file a.dot !\n");
		return;
	}
	
	if (verb)
		printf("start...\n");
	fprintf(f, "digraph %s\n{\n"\
	"	node[fontsize=20]"\
	"	edge[fontsize=20, arrowhead = open]"\
	"	rankdir = LR;\n"\
	"	size = \"%lf, %lf\";\n"\
	"	center = 1;\n"\
	"	nodesep = \"0.2\"\n", graph_name, sx, sy);
//	"	ranksep = \"0.4 equally\";\n", graph_name);
//	"	rotate = -90\n"\
//	"	orientation=landscape\n"\
//	"orientation = Landscape\n");
	if (verb)
		printf("write...\n");
	
	fprintf(f, "	\n");
	int i,j;
	for (i=0;i<a.n;i++)
	{
		fprintf(f, "	%d [shape=", i);
		if (a.e[i].final)
			fprintf(f, "doublecircle");
		else
			fprintf(f, "circle");
		fprintf(f, ", style=");
		if (a.e[i].initial)
			fprintf(f, "bold");
		else
			fprintf(f, "solid");
		fprintf(f, ", fontsize=20, margin=0]\n");
	}
	fprintf(f, "	\n");
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.e[i].n;j++)
		{
			if (a.e[i].a[j].e != -1)
			{
				if (a.e[i].a[j].l != -1)
					fprintf(f, "	%d -> %d [label=\"%s\"]\n", i, a.e[i].a[j].e, labels[a.e[i].a[j].l]);
				else
					fprintf(f, "	%d -> %d [label=\"Ɛ\"]\n", i, a.e[i].a[j].e);
			}
		}
	}
	fprintf(f, "}\n");
	
	fclose(f);
	if (run_dot)
	{
        if (verb)
            printf("draw...\n");
        sprintf(tamp, "dot %s -Gname -Tpng > %s.png", file, file);
        system(tamp);
	}
	//sprintf(tamp, "scp %s %s &> /dev/null", file, temp_dot_file_name); //copy the file in the choosen place
	//system(tamp);
}

//determine if the automaton is complete (i.e. with his sink state)
int IsCompleteAutomaton (Automaton a)
{
	int i,j;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] == -1)
				return 0;
		}
	}
	return 1;
}

//complete the automaton (i.e. add a sink state if necessary)
//return 1 iff a state was added
int CompleteAutomaton (Automaton *a)
{
	int ne = a->n; //new state
	int i,j;
	int add_state = 0;
	for (i=0;i<ne;i++)
	{
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] == -1)
			{
				a->e[i].f[j] = ne;
				add_state = 1;
			}
		}
	}
	if (a->i == -1)
	{
		a->i = ne;
		add_state = 1;
	}
	if (!add_state)
		return 0;
	AddState(a, 0); //add the sink state
	for (j=0;j<a->na;j++)
	{
		a->e[ne].f[j] = ne;
	}
	if (a->i == -1)
		a->i = ne;
	return 1;
}

//determine if the two automata are the same (different if permuted states)
int equalsAutomaton(Automaton a1, Automaton a2, int verb)
{
	if (a1.n != a2.n || a1.na != a2.na || a1.i != a2.i)
	{
	    if (verb)
    	    printf("n:(%d,%d) na:(%d,%d) i:(%d,%d)\n", a1.n, a2.n, a1.na, a2.na, a1.i, a2.i);
		return 0;
	}
	int i, j;
	for (i=0;i<a1.n;i++)
	{
		for (j=0;j<a1.na;j++)
		{
			if (a1.e[i].f[j] != a2.e[i].f[j])
			{
			    if (verb)
    			    printf("%d -%d-> %d in a1 but %d -%d-> %d in a2\n", i, j, a1.e[i].f[j], i, j, a2.e[i].f[j]);
				return 0;
			}
		}
		if (a1.e[i].final != a2.e[i].final)
		{
            if (verb)
	            printf("%d final and not final\n", i);
            return 0;
		}
	}
	if (verb)
	    printf("equals !\n");
	return 1;
}

//used by equalsLanguages
//determine if the languages of states e1 of a1 and state e2 of a2 are the same
int equalsLanguages_ind (Automaton a1, Automaton a2, Dict d, Dict a1toa2, Dict a2toa1, int e1, int e2, int verb)
{
    if (e1 >= d.n)
	{
	    printf("Error: we try to access to the element %d of the dictionnary of size %d.\n", e1, d.n);
	    return 0;
	}
	if (e1 >= a1.n)
	{
	    printf("Error: %d is not a state of a1 !\n", e1);
	}
	if (e2 >= a2.n)
	{
	    printf("Error: %d is not a state of a2 !\n", e2);
	}
	if ((a1.e[e1].final & 1) != (a2.e[e2].final & 1))
		return 0; //one of the states is final but not the other one
	if (d.e[e1] == e2)
	    return 1;
	if (d.e[e1] != -1)
	    return 0;
	d.e[e1] = e2;
	//browse the sons of e1 in a1
	int i;  
	for (i=0;i<a1.na;i++)
	{
		if (a1.e[e1].f[i] != -1)
		{//this edge exists in a1
			if (a1toa2.e[i] != -1)
			{
				if (a2.e[e2].f[a1toa2.e[i]] == -1)
				{//this edge doesn't correspond to an edge in a2
					if (verb)
						printf("%d -%d-> exists in a1 but %d -%d-> doesn't exists in a2.", e1, i, e2, a1toa2.e[i]);
					return 0;
				}
				if (!equalsLanguages_ind(a1, a2, d, a1toa2, a2toa1, a1.e[e1].f[i], a2.e[e2].f[a1toa2.e[i]], verb))
				{
					return 0;
				}
			}else
			{
				if (verb)
					printf("%d -%d-> exists in a1 but %d -%d-> doesn't exists in a2.", e1, i, e2, a1toa2.e[i]);
				return 0;
			}
		}else
		{
			if (a1toa2.e[i] != -1)
			{
				if (a2.e[e2].f[a1toa2.e[i]] != -1)
				{				
					if (verb)
						printf("%d -%d-> doesn't exists in a1 but %d -%d-> exists in a2.", e1, i, e2, a1toa2.e[i]);
					return 0;
				}
			}
		}
	}
	return 1;
}

//determine if the languages of the two automata are the same
//the dictionnary gives the letters of a2 depending of the ones of a1 (-1 if the letter of a1 doesn't correspond to any letter for a2).
//This dictionnary is assumed to be invertible.
//if minimized is 1, the automaton a1 and a2 are assumed to be minimal.
int equalsLanguages(Automaton *a1, Automaton *a2, Dict a1toa2, int minimized, int pruned, int verb)
{
	int i;
	Automaton a3 = *a1;
	Automaton a4 = *a2;
	int tofree = 0;
	if (!pruned)
	{
		if (verb)
			printf("Prune...\n");
		//prune the automata
		a3 = prune(a3, 0);
		a4 = prune(a4, 0);
		tofree = 1;
	}
	if (!minimized)
	{
		if (verb)
			printf("Minimize...\n");
		//minimize the automata
		Automaton a = Minimise(a3, 0);
		if (tofree)
    		FreeAutomaton(&a3);
    	a3 = a;
		a = Minimise(a4, 0);
		if (tofree)
		    FreeAutomaton(&a4);
		a4 = a;
		tofree = 1;
	}
	if (verb)
	{
		printf("Automata : ");
		printAutomaton(a3);
		printAutomaton(a4);
	}
	//
    if (a3.n != a4.n)
    {
        return 0;   
    }
	//inverse the dictionnary
	Dict a2toa1 = NewDict(a4.na);
	for (i=0;i<a1toa2.n;i++)
	{
		a2toa1.e[a1toa2.e[i]] = i;
	}
	if (verb)
		printDict(a2toa1);
	//Alloc the dict that goes from states of a1 to states of a2
	Dict d = NewDict(a3.n);
	for (i=0;i<a3.n;i++)
	{
	    d.e[i] = -1;
	}
	//
	int res;
	if (a3.i == -1 || a4.i == -1)
		res = (a3.i == a4.i);
	else
	{
		res = equalsLanguages_ind(a3, a4, d, a1toa2, a2toa1, a3.i, a4.i, verb);
	}
	//free memory
	FreeDict(&d);
	FreeDict(&a2toa1);
	if (tofree)
	{
	    FreeAutomaton(&a3);
	    FreeAutomaton(&a4);
	}
	return res;
}

//same as equalsLanguages but without induction
//determine if the languages of the two automata are the same
//the dictionnary gives the letters of a2 depending of the ones of a1 (-1 if the letter of a1 doesn't correspond to any letter for a2).
//This dictionnary is assumed to be invertible.
//if minimized is 1, the automaton a1 and a2 are assumed to be minimal.
int equalsLanguages2(Automaton *a1, Automaton *a2, Dict a1toa2, int minimized, int pruned, int verb)
{
	int i;
	if (!pruned)
	{
		if (verb)
			printf("Emonde...\n");
		//prun the automata
		Automaton a3 = prune(*a1, 0);
		FreeAutomaton(a1);
		*a1 = a3;
		a3 = prune(*a2, 0);
		FreeAutomaton(a2);
		*a2 = a3;
	}
	if (!minimized)
	{
		if (verb)
			printf("Minimise...\n");
		//minimise les automates
		Automaton a3 = Minimise(*a1, 0);
		FreeAutomaton(a1);
		*a1 = a3;
		a3 = Minimise(*a2, 0);
		FreeAutomaton(a2);
		*a2 = a3;
	}
	if (verb)
	{
		printf("Automata : ");
		printAutomaton(*a1);
		printAutomaton(*a2);
	}
	//inverse the dictionnary
	Dict a2toa1 = NewDict(a2->na);
	for (i=0;i<a1toa2.n;i++)
	{
		a2toa1.e[a1toa2.e[i]] = i;
	}
	if (verb)
		printDict(a2toa1);
	//
	int res = 1;
	if (a1->i == -1 || a2->i == -1)
		res = (a1->i == a2->i);
	else if (a1->n != a2->n)
	    res = 0;
	else
	{
		//browse the automata
		//alloc the stack
		int sp = log(a1->n) + 1; //size of allocated stack
		int cp = 0; //current position in the stack
		int *se1 = (int *)malloc(sizeof(int)*sp); //stack of current states of a1
		int *se2 = (int *)malloc(sizeof(int)*sp); //stack of current states of a2
		//res = equalsLanguages_ind(*a1, *a2, a1toa2, a2toa1, a1->i, a2->i, verb);
		se1[cp] = a1->i;
		se2[cp] = a2->i;
		int e1, e2;
		while(cp >= 0)
		{
		    e1 = se1[cp];
		    e2 = se2[cp];
		    cp--;
            if ((a1->e[e1].final & 1) != (a2->e[e2].final & 1))
            {    //return 0; //one of the states is final but not the other one
                res = 0;
                cp = -1;
                break;
            }
            if (a1->e[e1].final & 2 && a2->e[e2].final & 2)
            {
                //return 1; //state already seen
                continue;
            }
            //indicate that the state a has been seen
            a1->e[e1].final |= 2;
            a2->e[e2].final |= 2;
            //browse the sons of e1 in a1
            int i;
            for (i=0;i<a1->na;i++)
            {
                if (a1->e[e1].f[i] != -1)
                {//this edge exists in a1
                    if (a1toa2.e[i] != -1)
                    {
                        if (a2->e[e2].f[a1toa2.e[i]] == -1)
                        {//this edge doesn't correspond to an edge in a2
                            if (verb)
                                printf("%d -%d-> exists in a1 but %d -%d-> doesn't exists in a2.", e1, i, e2, a1toa2.e[i]);
                            //return 0;
                            res = 0;
                            cp = -1;
                            break;
                        }
                        //if (!equalsLanguages_ind(a1, a2, a1toa2, a2toa1, a1.e[e1].f[i], a2.e[e2].f[a1toa2.e[i]], verb))
                        //{
                        //    return 0;
                        //}
                        //add an element to the stack
                        cp++;
                        if (cp >= sp)
                        {
                            sp = min(sp*2, a1->n); //double the size of the stack
                            if (cp >= sp)
                            {
                                printf("Error : more elements than the size of the automaton in the stack !\n");
                                exit(1);
                            }
                            se1 = (int *)realloc(se1, sizeof(int)*sp);
                            se2 = (int *)realloc(se2, sizeof(int)*sp);
                        }
                        se1[cp] = a1->e[e1].f[i];
                        se2[cp] = a2->e[e2].f[a1toa2.e[i]];
                    }else
                    {
                        if (verb)
                            printf("%d -%d-> exists in a1 but %d -%d-> doesn't exists in a2.", e1, i, e2, a1toa2.e[i]);
                        //return 0;
                        cp = -1;
                        res = 0;
                        break;
                    }
                }else
                {
                    if (a1toa2.e[i] != -1)
                    {
                        if (a2->e[e2].f[a1toa2.e[i]] != -1)
                        {				
                            if (verb)
                                printf("%d -%d-> doesn't exists in a1 but %d -%d-> exists in a2.", e1, i, e2, a1toa2.e[i]);
                            //return 0;
                            cp = -1;
                            res = 0;
                            break;
                        }
                    }
                }
            }
        }
        //free the stack
        free(se1);
        free(se2);
	}
	//put back final states
	for (i=0;i<a1->n;i++)
	{
		a1->e[i].final &= 1;
	}
	for (i=0;i<a2->n;i++)
	{
		a2->e[i].final &= 1;
	}
	return res;
}

//used by emptyLanguage
//determine if the language of the state e is empty
int emptyLanguage_ind (Automaton a, int e)
{
	if (a.e[e].final)
		return 0;
	//indicate that the state has been seen
	a.e[e].final |= 2;
	//browse the sons
	int i;
	for (i=0;i<a.na;i++)
	{
		if (a.e[e].f[i] != -1)
		{
			if (a.e[a.e[e].f[i]].final & 2)
				continue; //this son was already seen
			if (!emptyLanguage_ind(a, a.e[e].f[i]))
				return 0;
		}
	}
	return 1;
}

//determine if the language of the automaton is empty
int emptyLanguage(Automaton a)
{
	if (a.i == -1)
		return 1;
	int res = emptyLanguage_ind(a, a.i);
	//put back final states
	int i;
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	return res;
}

//same as emptyLanguage but without induction
//determine if the language of the automaton is empty
int emptyLanguage2(Automaton a)
{
	if (a.i == -1)
		return 1;
	
	//int res = emptyLanguage_ind(a, a.i);
	int cp = 0; //current element in the stack
	int *se = (int *)malloc(sizeof(int)*a.n); //alloc the stack
	se[cp] = a.i;
	
	int e;
	int res = 1;
    while (cp >= 0)
    {
        e = se[cp];
        cp--;
        if (a.e[e].final)
        {
            res = 0;
            break;
            //return 0;
        }
        //indicate that the state has been seen
        a.e[e].final |= 2;
        //browse the sons
        int i;
        for (i=0;i<a.na;i++)
        {
            if (a.e[e].f[i] != -1)
            {
                if (a.e[a.e[e].f[i]].final & 2)
                    continue; //this son was already seen
                //if (!emptyLanguage_ind(a, a.e[e].f[i]))
                //    return 0;
                //add an element to the stack
                cp++;
                se[e] = a.e[e].f[i];
            }
        }
	}
	//free the stack
	free(se);
	
	//put back final states
	int i;
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	return res;
}

int findWord_ind (Automaton a, int e, int n, Dict *w, int verb)
{
	if (a.e[e].final)
	{
		if (verb)
			printf("Allocated one word of size %d.\n", n);
		*w = NewDict(n);
		return 1;
	}
	//indicate that the state a has been seen
	a.e[e].final |= 2;
	//browse sons
	int i;
	for (i=0;i<a.na;i++)
	{
		if (a.e[e].f[i] != -1)
		{
			if (a.e[a.e[e].f[i]].final & 2)
				continue; //this son was already seen
			if (findWord_ind(a, a.e[e].f[i], n+1, w, verb))
			{
				if (verb)
				{
					printf("w[%d] = %d\n", n, i);
				}
				w->e[n] = i;
				return 1;
			}
		}
	}
	return 0;
}

//return a word in the language of a
int findWord (Automaton a, Dict *w, int verb)
{
	if (a.i == -1)
		return 0;
	int res = findWord_ind(a, a.i, 0, w, verb);
	//put back final states
	int i;
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	return res;
}

/*
//return a word in the language of a
//same as findWord, but without induction
int findWord2 (Automaton a, Dict *w, int verb)
{
	if (a.i == -1)
		return 0;
	
	int sp = log(a.n)+2; //size of stack
	int cp = 0; //current index
	int *se = (int*)malloc(sizeof(int)*sp);
	int *sn = (int*)malloc(sizeof(int)*sp);
	int res = 0;
	//int res = findWord_ind(a, a.i, 0, w, verb);
	while (cp >= 0)
	{
	    //pop
	    e = se[cp];
	    n = sn[cp];
	    cp--;
	    if (a.e[e].final)
        {
            if (verb)
                printf("Allocated one word of size %d.\n", n);
            *w = NewDict(n);
            //return 1;
            res = 1;
            break;
        }
        //indicate that the state a has been seen
        a.e[e].final |= 2;
        //browse sons
        int i;
        for (i=0;i<a.na;i++)
        {
            if (a.e[e].f[i] != -1)
            {
                if (a.e[a.e[e].f[i]].final & 2)
                    continue; //this son was already seen
                
                /////
                if (findWord_ind(a, a.e[e].f[i], n+1, w, verb))
                {
                    if (verb)
                    {
                        printf("w[%d] = %d\n", n, i);
                    }
                    w->e[n] = i;
                    //return 1;
                    res = 1;
                    cp = -1;
                    break;
                }
                //////

                cp++;
                if (cp >= sp)
                {
                    sp = sp*2;
                    se = (int*)realloc(se, sizeof(int)*sp);
                    sn = (int*)realloc(sn, sizeof(int)*sn);
                }
                se[cp] = a.e[e].f[i];
                sn[cp] = n+1;
            }
        }
        //return 0;
	}
	
	//put back final states
	int i;
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	return res;
}
*/

//return a shortest word of the language
int shortestWord (Automaton a, Dict *w, int init, int end, int verb)
{
	if (init == -1)
		return 0;
	//Dijkstra's algorithm
	int *d = malloc(sizeof(int)*a.n); //table of distances from initial state
	int *prec = malloc(sizeof(int)*a.n); //table of predecessors
	int *vu = malloc(sizeof(int)*a.n);
	int i, j, imin, f;
	//initialization
	for (i=0;i<a.n;i++)
	{
		d[i] = a.n;
		prec[i] = -1;
		vu[i] = 0;
	}
	d[init] = 0;
	//Dijkstra (not very optimized)
	for (i=0;i<a.n;i++)
	{
		//find the nearest state not seen yet (could be optimized)
		imin = 0;
		while(vu[imin])
			imin++;
		for (j=0;j<a.n;j++)
		{
			if (d[j] < d[imin] && !vu[j])
			{
				imin = j;
			}
		}
		vu[imin] = 1;
		//browse sons
		for (j=0;j<a.na;j++)
		{
			f = a.e[imin].f[j];
			if (f != -1)
			{
				if (d[f] > d[imin]+1)
				{
					d[f] = d[imin]+1;
					prec[f] = imin;
				}
			}
		}
	}
	free(vu);
	//Determine the nearest final state (or end if end != -1)
	f = end;
	if (f == -1)
	{
		for (i=0;i<a.n;i++)
		{
			if (a.e[i].final)
			{
				if (f == -1)
					f = i;
				else if (d[i] < d[f])
				{
					f = i;
				}
			}
		}
	}
	free(d);
	if (f == -1)
	{
		free(prec);
		return 0;
	}
	//find the shortest path to this state
	i = 0;
	imin = f;
	while(prec[f] != -1)
	{
		i++;
		f = prec[f];
	}
	//alloc the word
	*w = NewDict(i);
	f = imin;
	while(prec[f] != -1)
	{
		i--;
		//find a letter to go from one state to the other
		for (j=0;j<a.na;j++)
		{
			if (a.e[prec[f]].f[j] == f)
			{
				w->e[i] = j;
				break;
			}
		}
		f = prec[f];
	}
	free(prec);
	return 1;
}

//return the shortest words up to each state
int shortestWords (Automaton a, Dict *w, int init, int verb)
{
	if (init == -1)
		return 0;
	//Dijkstra's algorithm
	int *d = malloc(sizeof(int)*a.n); //table of distances from the initial state
	int *prec = malloc(sizeof(int)*a.n); //table of predecessors
	int *vu = malloc(sizeof(int)*a.n);
	int i, j, k, imin, f;
	//initialization
	for (i=0;i<a.n;i++)
	{
		d[i] = a.n;
		prec[i] = -1;
		vu[i] = 0;
	}
	d[init] = 0;
	if (verb)
		printf("Dijkstra...\n");
	//Dijkstra (not very well optimized)
	for (i=0;i<a.n;i++)
	{
		//find the nearest state not already seeen (could be optimized)
		imin = 0;
		while(vu[imin])
			imin++;
		for (j=0;j<a.n;j++)
		{
			if (d[j] < d[imin] && !vu[j])
			{
				imin = j;
			}
		}
		vu[imin] = 1;
		//browse sons
		for (j=0;j<a.na;j++)
		{
			f = a.e[imin].f[j];
			if (f != -1)
			{
				if (d[f] > d[imin]+1)
				{
					d[f] = d[imin]+1;
					prec[f] = imin;
				}
			}
		}
	}
	free(vu);
	if (verb)
	{
		for (i=0;i<a.n;i++)
		{
			printf("prec[%d] = %d, d[%d] = %d\n", i, prec[i], i, d[i]);
		}
	}
	if (verb)
		printf("Fill the list...\n");
	//browse the states
	for (k=0;k<a.n;k++)
	{
		//find the shortest path to this state
		//find the length of the path
		i = 0;
		f = k;
		while(prec[f] != -1)
		{
			i++;
			f = prec[f];
		}
		if (verb)
			printf("alloc %d (size %d)...\n", k, i);
		//alloc the word
		w[k] = NewDict(i);
		f = k;
		while(prec[f] != -1)
		{
			i--;
			//find a letter to go from one state to the next one
			for (j=0;j<a.na;j++)
			{
				if (a.e[prec[f]].f[j] == f)
				{
					w[k].e[i] = j;
					break;
				}
			}
			f = prec[f];
		}
	}
	if (verb)
		printf("end...\n");
	free(prec);
	return 1;
}

//check that the word w is recognized by the automaton
int rec_word(Automaton a, Dict d)
{
	int i;
	int e = a.i;
    if (e == -1)
	{
		return 0;
	}
	for (i=0;i<d.n;i++)
	{
		e = a.e[e].f[d.e[i]];
		if (e == -1)
		{
			return 0;
		}
	}
	return a.e[e].final;
}

int contract (int i1, int i2, int n1)
{
	return i1+n1*i2;
}

int geti1 (int c, int n1)
{
	return c%n1;
}

int geti2 (int c, int n1)
{
	return c/n1;
}

void Product_ind(Automaton r, int i1, int i2, Automaton a1, Automaton a2, Dict d)
{
	int i,j;
	int e1, e2;
	int a;
	State *current = &r.e[contract(i1, i2, a1.n)];
	int *next;
	current->final = 1; //indicate that the state has been visited
	for (i=0;i<a1.na;i++)
	{
		e1 = a1.e[i1].f[i];
		if (e1 < 0)
			continue;
		for (j=0;j<a2.na;j++)
		{
			e2 = a2.e[i2].f[j];
			a = d.e[contract(i,j,a1.na)];
			next = &current->f[a];
			if (a != -1)
			{
				if (e2 < 0)
					*next = -1;
				else
				{
					*next = contract(e1, e2, a1.n);
					if (!r.e[*next].final)
						Product_ind(r, e1, e2, a1, a2, d);
				}
			}
		}
	}
}

Automaton Product(Automaton a1, Automaton a2, Dict d, int verb)
{
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	//count the number of letters of the final alphabet
	int i, na=0;
	for (i=0;i<d.n;i++)
	{
		if (d.e[i] >= na)
			na = d.e[i]+1;
	}
	Automaton r = NewAutomaton(a1.n*a2.n, na);
	initAutomaton(&r);
	if (a1.i == -1 || a2.i == -1)
	{
		r.i = -1;
		return r;
	}
	r.i = contract(a1.i, a2.i, a1.n);
	Product_ind(r, a1.i, a2.i, a1, a2, d);
	//put the final states
	for (i=0;i<r.n;i++)
	{
		r.e[i].final = a1.e[geti1(i, a1.n)].final && a2.e[geti2(i, a1.n)].final;
	}
	fflush(stdout);
	return r;
}

//same as Product, but without induction
Automaton Product2(Automaton a1, Automaton a2, Dict d, int verb)
{
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	//count the number of letters of the final alphabet
	int i, na=0;
	for (i=0;i<d.n;i++)
	{
		if (d.e[i] >= na)
			na = d.e[i]+1;
	}
	Automaton r = NewAutomaton(a1.n*a2.n, na);
	initAutomaton(&r);
	if (a1.i == -1 || a2.i == -1)
	{
		r.i = -1;
		return r;
	}
	r.i = contract(a1.i, a2.i, a1.n);
	
	//Product_ind(r, a1.i, a2.i, a1, a2, d);
	int cp = 0; //current element of the stack
	int sp = log(a1.n)+2; //allocated size of the stack
	int *se1 = (int *)malloc(sizeof(int)*sp); //alloc the stack
	int *se2 = (int *)malloc(sizeof(int)*sp);
	se1[cp] = a1.i;
	se2[cp] = a2.i;
	int i1, i2;
	while (cp >= 0)
	{
	    i1 = se1[cp];
	    i2 = se2[cp];
	    cp--;
        int j;
        int e1, e2;
        int a;
        State *current = &r.e[contract(i1, i2, a1.n)];
        int *next;
        current->final = 1; //indicate that the state has been visited
        for (i=0;i<a1.na;i++)
        {
            e1 = a1.e[i1].f[i];
            if (e1 < 0)
                continue;
            for (j=0;j<a2.na;j++)
            {
                e2 = a2.e[i2].f[j];
                a = d.e[contract(i,j,a1.na)];
                next = &current->f[a];
                if (a != -1)
                {
                    if (e2 < 0)
                        *next = -1;
                    else
                    {
                        *next = contract(e1, e2, a1.n);
                        if (!r.e[*next].final)
                        {
                            //Product_ind(r, e1, e2, a1, a2, d);
                            cp++;
                            if (cp >= sp)
                            {
                                //double the size of the stack
                                sp = sp*2;
                                se1 = (int *)realloc(se1, sizeof(int)*sp);
                                se2 = (int *)realloc(se2, sizeof(int)*sp);
                            }
                            se1[cp] = e1;
                            se2[cp] = e2;
                        }
                    }
                }
            }
        }
    }
    //free the stack
    free(se1);
    free(se2);
    
	//put the final states
	for (i=0;i<r.n;i++)
	{
		r.e[i].final = a1.e[geti1(i, a1.n)].final && a2.e[geti2(i, a1.n)].final;
	}
	return r;
}

int Intersect_ind(int i1, int i2, Automaton a1, Automaton a2, int *vu, int verb)
{
	if (verb)
		printf("Intersect_ind %d %d...\n", i1, i2);
	int i,j;
	int e1, e2;
	if (a1.e[i1].final && a2.e[i2].final)
		return 1;
	int a = contract(i1, i2, a1.n);
	if (vu[a])
		return 0;
	vu[a] = 1; //indicate that the state has been visited
	for (i=0;i<a1.na;i++)
	{
		e1 = a1.e[i1].f[i];
		if (e1 < 0)
			continue;
		e2 = a2.e[i2].f[i];
		if (e2 < 0)
			continue;
		if (Intersect_ind(e1, e2, a1, a2, vu, verb))
			return 1;
	}
	return 0;
}

//determine if the intersection is empty
int Intersect (Automaton a1, Automaton a2, int verb)
{
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	if (a1.i == -1 || a2.i == -1)
	{
		if (verb)
			printf("One of the automata doesn't have an initial state !\n");
		return 0;
	}
	int *vu = (int *)malloc(sizeof(int)*a1.n*a2.n);
	int i;
	for (i=0;i<a1.n*a2.n;i++)
		vu[i] = 0;
	int res = Intersect_ind(a1.i, a2.i, a1, a2, vu, verb);
	free(vu);
	return res;
}

//determine if the intersection is empty
//same as Intersect, but without induction
int Intersect2 (Automaton a1, Automaton a2, int verb)
{
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	if (a1.i == -1 || a2.i == -1)
	{
		if (verb)
			printf("One of the automata doesn't have an initial state !\n");
		return 0;
	}
	int *vu = (int *)malloc(sizeof(int)*a1.n*a2.n);
	int i;
	for (i=0;i<a1.n*a2.n;i++)
		vu[i] = 0;
	int res = 0;
	int sp = log(a1.n)+2; //allocated size of stack
	int cp = 0; //current index in the stack
	int *se1 = (int *)malloc(sizeof(int)*sp); //alloc the stack
	int *se2 = (int *)malloc(sizeof(int)*sp);
	//res = Intersect_ind(a1.i, a2.i, a1, a2, vu, verb);
	se1[cp] = a1.i;
	se2[cp] = a2.i;
	int i1, i2;
	while(cp >= 0)
	{
	    i1 = se1[cp];
	    i2 = se2[cp];
	    cp--;
        if (verb)
            printf("Intersect_ind %d %d...\n", i1, i2);
        int i,j;
        int e1, e2;
        if (a1.e[i1].final && a2.e[i2].final)
        {
            res = 1;
            break;
            //return 1;
        }
        int a = contract(i1, i2, a1.n);
        if (vu[a])
            return 0;
        vu[a] = 1; //indicate that the state has been visited
        for (i=0;i<a1.na;i++)
        {
            e1 = a1.e[i1].f[i];
            if (e1 < 0)
                continue;
            e2 = a2.e[i2].f[i];
            if (e2 < 0)
                continue;
            //if (Intersect_ind(e1, e2, a1, a2, vu, verb))
            //    return 1;
            cp++;
            if (cp >= sp)
            {
                sp = sp*2;
                se1 = (int *)realloc(se1, sizeof(int)*sp);
                se2 = (int *)realloc(se2, sizeof(int)*sp);
            }
            se1[cp] = e1;
            se2[cp] = e2;
        }
        return 0;
    }
    //free the stack
    free(se1);
    free(se2);
    
	free(vu);
	return res;
}

int Included_ind(int i1, int i2, Automaton a1, Automaton a2, int *vu)
{
	int i,j;
	int e1, e2;
	if (a1.e[i1].final && !a2.e[i2].final)
		return 0;
	int a = contract(i1, i2, a1.n);
	if (vu[a])
		return 1;
	vu[a] = 1; //indicate that the state has been visited
	for (i=0;i<a1.na;i++)
	{
		e1 = a1.e[i1].f[i];
		if (e1 < 0)
			continue;
		if (i >= a2.na)
			return 0;
		e2 = a2.e[i2].f[i];
		if (e2 < 0)
			return 0;
		if (!Included_ind(e1, e2, a1, a2, vu))
			return 0;
	}
	return 1;
}

//determine if the language of a1 is included in the language of a2
int Included(Automaton a1, Automaton a2, int pruned, int verb)
{
	if (!pruned)
	{
		a1 = prune(a1, verb);
	}
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	if (a1.i == -1)
		return 1;
	if (a2.i == -1)
		return emptyLanguage(a1);
	int *vu = (int *)malloc(sizeof(int)*a1.n*a2.n);
	int i;
	for (i=0;i<a1.n*a2.n;i++)
		vu[i] = 0;
	int res = Included_ind(a1.i, a2.i, a1, a2, vu);
	free(vu);
	return res;
}

//determine if the language of a1 is included in the language of a2
//same as Included, but without induction
int Included2(Automaton a1, Automaton a2, int pruned, int verb)
{
	if (!pruned)
	{
		a1 = prune(a1, verb);
	}
	if (verb)
	{
		printAutomaton(a1);
		printAutomaton(a2);
	}
	if (a1.i == -1)
		return 1;
	if (a2.i == -1)
		return emptyLanguage(a1);
	int *vu = (int *)malloc(sizeof(int)*a1.n*a2.n);
	int i,j;
	for (i=0;i<a1.n*a2.n;i++)
		vu[i] = 0;
	int cp = 0; //current index in the stack
	int sp = log(a1.n)+2; //allocated size of the stack
	int *se1 = (int *)malloc(sizeof(int)*sp); //alloc the stack
	int *se2 = (int *)malloc(sizeof(int)*sp);
	//int res = Included_ind(a1.i, a2.i, a1, a2, vu);
	se1[cp] = a1.i;
	se2[cp] = a2.i;
	int e1, e2;
	int i1, i2;
	int res = 1;
	while (cp >= 0)
	{
	    //pop
	    i1 = se1[cp];
	    i2 = se2[cp];
	    cp--;
        if (a1.e[i1].final && !a2.e[i2].final)
        {
            //return 0;
            res = 0;
            break;
        }
        int a = contract(i1, i2, a1.n);
        if (vu[a])
        {
            //return 1;
            continue;
        }
        vu[a] = 1; //indicate that the state has been visited
        for (i=0;i<a1.na;i++)
        {
            e1 = a1.e[i1].f[i];
            if (e1 < 0)
                continue;
            if (i >= a2.na)
                return 0;
            e2 = a2.e[i2].f[i];
            if (e2 < 0)
                return 0;
            //if (!Included_ind(e1, e2, a1, a2, vu))
            //    return 0;
            cp++;
            if (cp >= sp)
            {
                //double the stack
                sp = sp*2;
                se1 = (int*)realloc(se1, sizeof(int)*sp);
                se2 = (int*)realloc(se2, sizeof(int)*sp);
            }
            se1[cp] = e1;
            se2[cp] = e2;
        }
        return 1;
    }
    //free the stack
    free(se1);
    free(se2);
    
	free(vu);
	return res;
}

void AddState (Automaton *a, int final)
{
	a->n++;
	if (a->n == 1)
		a->e = (State *)malloc(sizeof(State));
	else
		a->e = (State *)realloc(a->e, sizeof(State)*a->n);
	if (!a->e)
	{
		printf("Out of memory !");
		exit(2);
	}
	a->e[a->n-1].f = (int *)malloc(sizeof(int)*a->na);
	if (!a->e[a->n-1].f)
	{
		printf("Out of memory !");
		exit(3);
	}
	int i;
	for (i=0;i<a->na;i++)
	{
		a->e[a->n-1].f[i] = -1;
	}
	a->e[a->n-1].final = final;
}

States NewStates (int n)
{
	States e;
	e.n = n;
	e.e = (int *)malloc(sizeof(int)*n);
	if (!e.e)
	{
		printf("Out of memory !");
		exit(7);
	}
return e;
}

void FreeStates (States e)
{
	free(e.e);
}

void initStates (States e)
{
	int i;
	for (i=0;i<e.n;i++)
	{
		e.e[i] = 0;
	}
}

void printStates (States e)
{
	int i;
	printf("[ ");
	for (i=0;i<e.n;i++)
	{
		printf("%d ", e.e[i]);
		fflush(stdout);
	}
	printf("]\n");
}

int equals (States e1, States e2)
{
	if (e1.n != e2.n)
		return 0;
	int i;
	for (i=0;i<e1.n;i++)
	{
		if (e1.e[i] != e2.e[i])
			return 0;
	}
	return 1;
}

States copyStates(States e)
{
	States r = NewStates(e.n);
	int i;
	for (i=0;i<e.n;i++)
	{
		r.e[i] = e.e[i];
	}
	return r;
}

void printListStates (ListStates l)
{
	int i;
	for (i=0;i<l.n;i++)
	{
		printf("%d : ", i);
		printStates(l.e[i]);
	}
}

//add an element if not already in the list
int AddEl (ListStates *l, States e, int* res)
{
	int i;
	for (i=0;i<l->n;i++)
	{
		if (equals(l->e[i], e))
		{
			if (res)
				*res = i;
			return 0;
		}
	}
	//add the element
	l->n++;
	if (l->n == 1)
		l->e = (States*)malloc(sizeof(States));
	else
		l->e = (States*)realloc(l->e, sizeof(States)*l->n);
	if (!l->e)
	{
		printf("Out of memory !");
		exit(4);
	}
	l->e[l->n-1] = copyStates(e);
	if (res)
		*res = l->n-1;
	return 1;
}

//add an element even if already in the list
void AddEl2 (ListStates *l, States e)
{
	//add the element
	l->n++;
	if (l->n == 1)
		l->e = (States*)malloc(sizeof(States));
	else
		l->e = (States*)realloc(l->e, sizeof(States)*l->n);
	if (!l->e)
	{
		printf("Out of memory !");
		exit(5);
	}
	l->e[l->n-1] = copyStates(e);
}

///////////////////////////////////////////////////////////////////
States2 NewStates2 (int n)
{
	States2 e;
	e.n = n;
	e.e = (uint64 *)malloc(sizeof(uint64)*((n+63)/64));
	if (!e.e)
	{
		printf("Out of memory !");
		exit(7);
	}
return e;
}

void FreeStates2 (States2 e)
{
	free(e.e);
}

void initStates2 (States2 e)
{
	int i;
	int n = (e.n+63)/64;
	for (i=0;i<n;i++)
	{
		e.e[i] = 0;
	}
}

void printStates2 (States2 e)
{
	int i, j;
	int n = (e.n+63)/64;
	printf("[ ");
	for (i=0;i<n;i++)
	{
		for (j=0;j<64;j++)
		{
			if (e.e[i] & (uint64)1<<j)
			{
				printf("%d ", 64*i+j);
				fflush(stdout);
			}
		}
	}
	printf("]\n");
}

int isNullStates2 (States2 e)
{
	int i;
	int n = (e.n+63)/64;
	for (i=0;i<n;i++)
	{
		if (e.e[i] != 0)
			return 0;
	}
	return 1;
}

int equalsStates2 (States2 e1, States2 e2)
{
	if (e1.n != e2.n)
		return 0;
	int i;
	int n = (e1.n+63)/64;
	for (i=0;i<n;i++)
	{
		if (e1.e[i] != e2.e[i])
			return 0;
	}
	return 1;
}

int hasStates2(States2 e, uint64 i)
{
	return (e.e[i/64] & ((uint64)1<<(i%64))) != 0;
}

States2 copyStates2(States2 e)
{
	States2 r = NewStates2(e.n);
	int i;
	int n = (e.n+63)/64;
	for (i=0;i<n;i++)
	{
		r.e[i] = e.e[i];
	}
	return r;
}

void addState (States2 *e, uint64 i)
{
	e->e[i/64] |= ((uint64)1<<(i%64));
}

ListStates2 NewListStates2 (int n, int na)
{
	ListStates2 r;
	r.n = n;
	r.na = na;
	r.e = (States2*)malloc(sizeof(States2)*na);
	return r;	
}

void ReallocListStates2(ListStates2 *l, int n, int marge)
{
	if (!marge)
	{
		if (l->na)
			l->e = (States2*)realloc(l->e, sizeof(States2)*n);
		else
			l->e = (States2*)malloc(sizeof(States2)*n);
		l->na = n;
	}else
	{
		if (n > l->na)
		{
			if (l->na)
				l->e = (States2*)realloc(l->e, sizeof(States2)*n*2);
			else
				l->e = (States2*)malloc(sizeof(States2)*n*2);
			l->na = n*2;
		}
	}
	l->n = n;
}

void FreeListStates2 (ListStates2* l)
{
	int i;
	for (i=0;i<l->n;i++)
	{
		FreeStates2(l->e[i]);
	}
	free(l->e);
	l->n = 0;
	l->na = 0;
}

void printListStates2 (ListStates2 l)
{
	int i;
	for (i=0;i<l.n;i++)
	{
		printf("%d : ", i);
		printStates2(l.e[i]);
	}
	printf("(%d allocated states2 )\n", l.na);
}

///////////////////////////////////////////////////////////////////

Dict* lhash;
const int nhash = 10000019;
int allocated = 0;
int filled = 0;

void AllocHash (void)
{
	if (!allocated)
	{
		lhash = (Dict*)malloc(sizeof(Dict)*nhash);
		if (!lhash)
		{
				printf("Out of memory !");
			exit(8);
		}
		allocated = 1;
	}
	if (!filled)
	{
		int i;
		for (i=0;i<nhash;i++)
		{
			lhash[i].e = NULL;
			lhash[i].n = 0;
		}
		filled = 1;
	}
}

void FreeHash (void)
{
	free(lhash);
	allocated = 0;
	filled = 0;
}

int hashStates (States e)
{
	int i;
	int h = 1;
	for (i=0;i<e.n;i++)
	{
		h *= 2;
		h += e.e[i];
		h %= nhash;
	}
	return h;
}

int hash2 (States2 e)
{
	int i;
	uint64 h = 1;
	int n = (e.n+63)/64;
	for (i=0;i<n;i++)
	{
		h *= 2;
		h += e.e[i];
		h %= nhash;
	}
	return h;
}

//add the element if not already in the hash table
int addStates2 (const ListStates2* l, States2 e, int *k)
{
	int h = hash2(e);
	int i, v;
	for (i=0;i<lhash[h].n;i++)
	{
		////////check
		if (lhash[h].e[i] >= l->n)
		{
			printf("***************\nError : element of the hash table too big !!!\n****************\n");
		}
		/////////////
		v = lhash[h].e[i];
		if (k)
			*k = v;
		if (equalsStates2(l->e[v], e))
		{
			//printf("equals !\n");
			return 0;
		}
	}
	//add the element
	if (k)
		*k = l->n;
	dictAdd(&lhash[h], l->n);
	return 1;
}

//add the element if not already in the hash table
int addH (const ListStates *l, States e, int* nf)
{
	int h = hashStates(e);
	
	int i, v;
	for (i=0;i<lhash[h].n;i++)
	{
		////////verif
		if (lhash[h].e[i] >= l->n)
		{
			printf("***************\nError : element of the hash table too big !!!\n****************\n");
		}
		/////////////
		v = lhash[h].e[i];
		if (nf)
			*nf = v;
		if (v < 0)
			return 0;
		if (equals(l->e[v], e))
		{
			//printf("equals !\n");
			return 0;
		}
	}
	//add the element
	if (nf)
		*nf = l->n;
	dictAdd(&lhash[h], l->n);
	return 1;
}

InvertDict NewInvertDict(int n)
{
	InvertDict r;
	r.n = n;
	if (n == 0)
		return r;
	r.d = (Dict*)malloc(sizeof(Dict)*n);
	if (!r.d)
	{
		printf("Out of memory !");
		exit(9);
	}
	return r;
}

InvertDict invertDict(Dict d)
{
	//count the number of different values (assumed to be consecutive)
	int i;
	int nv = 0;
	for (i=0;i<d.n;i++)
	{
		if (d.e[i] >= nv)
			nv = d.e[i]+1;
	}
	//alloc the inverse
	InvertDict r;
	r.n = nv;
	r.d = (Dict *)malloc(sizeof(Dict)*nv);
	if (!r.d)
	{
		printf("Out of memory !");
		exit(10);
	}
	//initialize
	for (i=0;i<nv;i++)
	{
		r.d[i].n = 0;
		r.d[i].e = NULL;
	}
	//fill the dictionnary
	for (i=0;i<d.n;i++)
	{
		if (d.e[i] != -1)
			dictAdd(&r.d[d.e[i]], i);
	}
	return r;
}

void FreeInvertDict(InvertDict id)
{
	if (id.n == 0)
		return;
	int i;
	for (i=0;i<id.n;i++)
	{
		FreeDict(&id.d[i]);
	}
	free(id.d);
}

void printInvertDict (InvertDict id)
{
	int i;
	for (i=0;i<id.n;i++)
	{
		printf("%d : ", i);
		printDict(id.d[i]);
	}
}

////////////////////////////////// to improve with a hash table !!!!
void putState (States *f, int ef)
{
	int i;
	for (i=0;i<f->n;i++)
	{
		if (f->e[i] == ef)
			return;
	}
	f->e[f->n] = ef;
	f->n++;
}

//function used by Determinize()
//States : list of states of a
void Determinize_ind (Automaton a, InvertDict id, Automaton *r, ListStates* l, int onlyfinals, int nof, int niter)
{
	int current = l->n-1;
	States c = l->e[current];
	//Browse sons
	States f = NewStates(a.n);
	int nf;
	State e;
	int i,j,k;
	int ef;
	int final;
	
	for (i=0;i<id.n;i++) //browse letters of the new alphabet
	{
		//fill f (list of states of a corresponding to the state of r where we come)
		f.n = 0;
		final = 0;
		for (j=0;j<c.n;j++) //browse the states of the list
		{
			e = a.e[c.e[j]]; //corresponding state
			for (k=0;k<id.d[i].n;k++) //browse the original letters, corresponding to the new chosen letter
			{
				ef = e.f[id.d[i].e[k]];
				if (ef != -1)
				{
					//check that the state of a is not already in the list
					putState(&f, ef);
					if (a.e[ef].final)
						final = 1;
				}
			}
		}
		if (onlyfinals && !final)
			continue;
		if (nof && final)
			continue;
		//test if the state has been seen, and otherwise mark it as seen
		if (addH(l, f, &nf)) //add the state to the hash table if new
		{	
			//add the state to the list
			AddEl2(l, f);
			//add the state to r
			if (nof)
				final = 1;
			AddState(r, final);
			//induction
			Determinize_ind(a, id, r, l, onlyfinals, nof, niter+1);
		}
		if (nf != -1)
		{
			//add the edge
			r->e[current].f[i] = nf;
		}
	}
	FreeStates(f);
}

//Determinize the automaton obtained by changing the alphabet, using the Power Set Construction.
Automaton Determinize(Automaton a, Dict d, int noempty, int onlyfinals, int nof, int verb)
{
	int i;
	
	Automaton r;
	if (a.i == -1)
	{
		//compute the size of the alphabet
		int nv = 0;
		for (i=0;i<d.n;i++)
		{
			if (d.e[i] >= nv)
				nv = d.e[i]+1;
		}
		//
		if (verb)
			printf("No initial state !\n");
		if (nof)
		{
			r = NewAutomaton(1, nv);
			r.i = 0;
			r.e[0].final = 1;
			for (i=0;i<nv;i++)
			{
				r.e[0].f[i] = 0;
			}
		}else
			r = NewAutomaton(0, nv);
		return r;
	}
	
/*
	//increase the stack size
	const rlim_t kStackSize = 32 * 1024 * 1024;
	struct rlimit rl;
	int result;
	result = getrlimit(RLIMIT_STACK, &rl);
	if (result == 0)
	{
		if (rl.rlim_cur < kStackSize)
		{
			if (verb)
				printf("limite : %d -> %d\n", rl.rlim_cur, kStackSize);
			rl.rlim_cur = kStackSize;
			result = setrlimit(RLIMIT_STACK, &rl);
			if (result != 0)
			{
				fprintf(stderr, "setrlimit returned result = %d\n", result);
			}
		}
	}
	//
*/
	
	if (verb)
	{
		if (onlyfinals)
			printf("onlyfinals\n");
		if (nof)
			printf("nof\n");
		if (noempty)
			printf("noempty\n");
		printf("Dictionary : ");
		printDict(d);
	}
	
	//compute the inverse of the dictionnary
	InvertDict id = invertDict(d);
	if (verb && id.n == d.n)
	{
		printf("The dictionary is inversible : trivial determination !\n");
	}
	
	if (verb)
	{
		printf("Inverse Dictionary :\n");
		printInvertDict(id);
	}
	
	//alloc the hash table
	AllocHash();
	//put the empty set in the hash table if we don't want this state in r
	if (noempty)
	{
		States e = NewStates(0); //empty set
		int h = hashStates(e);
		if (verb)
			printf("hash empty : %d\n", h);
		dictAdd(&lhash[h], -1);
	}
	
	//initialize the result automaton with just the initial state
	if (verb)
		printf("Init r...\n");
	r.n = 1;
	r.na = id.n;
	r.i = 0;
	r.e = (State *)malloc(sizeof(State));
	if (!r.e)
	{
		printf("Out of memory !");
		exit(11);
	}
	if (nof)
		r.e[0].final = 1;
	else
		r.e[0].final = a.e[a.i].final;
	r.e[0].f = (int *)malloc(sizeof(int)*r.na);
	if (!r.e[0].f)
	{
		printf("Out of memory !");
		exit(12);
	}
	for (i=0;i<r.na;i++)
	{
		r.e[0].f[i] = -1;
	}
	if (verb)
		printAutomaton(r);
	
	//initialize the list of states of the new automaton and the hash table
	//(this list is used to number with consecutive numbers the states of the new automaton that are list of states of a)
	if (verb)
		printf("Init l...\n");
	ListStates l;
	l.n = 0;
	l.e = NULL;
	States e = NewStates(1);
	e.e[0] = a.i; //the initial state of the new automaton is the list of initial states (here with cardinality 1)
	addH(&l, e, NULL);
	AddEl2(&l, e);
	
	//initialize the hash table
	int b = addH(&l, l.e[0], NULL); //add the initial state to the hash table
	if (verb)
		printListStates(l);
	
	if (verb)
		printf("Induction...\n");
	
	Determinize_ind(a, id, &r, &l, onlyfinals, nof, 0);
	
	if (verb)
		printf("Free...\n");
	
	//put back to zero the element of the hash table
	for (i=0;i<l.n;i++)
	{
		FreeDict(&lhash[hashStates(l.e[i])]);
	}
	
	for (i=0;i<l.n;i++)
	{
		FreeStates(l.e[i]);
	}
	free(l.e);
	
	FreeInvertDict(id);
	//FreeHash(); //do not free the memory, in order to use it faster after
	
	return r;
}

//Determinize the automaton obtained by changing the alphabet, using the Power Set Construction.
//same as Determinize, but without induction
Automaton Determinize2(Automaton a, Dict d, int noempty, int onlyfinals, int nof, int verb)
{
	int i;
	
	Automaton r;
	if (a.i == -1)
	{
		//compute the size of the alphabet
		int nv = 0;
		for (i=0;i<d.n;i++)
		{
			if (d.e[i] >= nv)
				nv = d.e[i]+1;
		}
		//
		if (verb)
			printf("No initial state !\n");
		if (nof)
		{
			r = NewAutomaton(1, nv);
			r.i = 0;
			r.e[0].final = 1;
			for (i=0;i<nv;i++)
			{
				r.e[0].f[i] = 0;
			}
		}else
			r = NewAutomaton(0, nv);
		return r;
	}
	
	if (verb)
	{
		if (onlyfinals)
			printf("onlyfinals\n");
		if (nof)
			printf("nof\n");
		if (noempty)
			printf("noempty\n");
		printf("Dictionary : ");
		printDict(d);
	}
	
	//compute the inverse of the dictionnary
	InvertDict id = invertDict(d);
	if (verb && id.n == d.n)
	{
		printf("The dictionary is inversible : trivial determination !\n");
	}
	
	if (verb)
	{
		printf("Inverse Dictionary :\n");
		printInvertDict(id);
	}
	
	//alloc the hash table
	AllocHash();
	//put the empty set in the hash table if we don't want this state in r
	if (noempty)
	{
		States e = NewStates(0); //empty set
		int h = hashStates(e);
		if (verb)
			printf("hash empty : %d\n", h);
		dictAdd(&lhash[h], -1);
	}
	
	//initialize the result automaton with just the initial state
	if (verb)
		printf("Init r...\n");
	r.n = 1;
	r.na = id.n;
	r.i = 0;
	r.e = (State *)malloc(sizeof(State));
	if (!r.e)
	{
		printf("Out of memory !");
		exit(11);
	}
	if (nof)
		r.e[0].final = 1;
	else
		r.e[0].final = a.e[a.i].final;
	r.e[0].f = (int *)malloc(sizeof(int)*r.na);
	if (!r.e[0].f)
	{
		printf("Out of memory !");
		exit(12);
	}
	for (i=0;i<r.na;i++)
	{
		r.e[0].f[i] = -1;
	}
	if (verb)
		printAutomaton(r);
	
	//initialize the list of states of the new automaton and the hash table
	//(this list is used to number with consecutive numbers the states of the new automaton that are list of states of a)
	if (verb)
		printf("Init l...\n");
	ListStates l;
	l.n = 0;
	l.e = NULL;
	States e = NewStates(1);
	e.e[0] = a.i; //the initial state of the new automaton is the list of initial states (here with cardinality 1)
	addH(&l, e, NULL);
	AddEl2(&l, e);
	
	//initialize the hash table
	int b = addH(&l, l.e[0], NULL); //add the initial state to the hash table
	if (verb)
		printListStates(l);
	
	if (verb)
		printf("Induction...\n");
	
	int cp = 0; //current index in the stack
	//Determinize_ind(a, id, &r, &l, onlyfinals, nof, 0);
	while (cp >= 0)
	{
	    cp--;
        int current = l.n-1;
        States c = l.e[current];
        //Browse sons
        States f = NewStates(a.n);
        int nf;
        State e;
        int i,j,k;
        int ef;
        int final;
    
        for (i=0;i<id.n;i++) //browse letters of the new alphabet
        {
            //fill f (list of states of a corresponding to the state of r where we come)
            f.n = 0;
            final = 0;
            for (j=0;j<c.n;j++) //browse the states of the list
            {
                e = a.e[c.e[j]]; //corresponding state
                for (k=0;k<id.d[i].n;k++) //browse the original letters, corresponding to the new chosen letter
                {
                    ef = e.f[id.d[i].e[k]];
                    if (ef != -1)
                    {
                        //check that the state of a is not already in the list
                        putState(&f, ef);
                        if (a.e[ef].final)
                            final = 1;
                    }
                }
            }
            if (onlyfinals && !final)
                continue;
            if (nof && final)
                continue;
            //test if the state has been seen, and otherwise mark it as seen
            if (addH(&l, f, &nf)) //add the state to the hash table if new
            {	
                //add the state to the list
                AddEl2(&l, f);
                //add the state to r
                if (nof)
                    final = 1;
                AddState(&r, final);
                //induction
                //Determinize_ind(a, id, r, l, onlyfinals, nof, niter+1);
                cp++;
            }
            if (nf != -1)
            {
                //add the edge
                r.e[current].f[i] = nf;
            }
        }
        FreeStates(f);
    }
    
	if (verb)
		printf("Free...\n");
	
	//put back to zero the element of the hash table
	for (i=0;i<l.n;i++)
	{
		FreeDict(&lhash[hashStates(l.e[i])]);
	}
	
	for (i=0;i<l.n;i++)
	{
		FreeStates(l.e[i]);
	}
	free(l.e);
	
	FreeInvertDict(id);
	//FreeHash(); //do not free the memory, in order to use it faster after
	
	return r;
}

NAutomaton Concat (Automaton a, Automaton b, int verb)
{
	int i, j, f;
	// !!! should take care of the fact that alphabet could be differents !!!
	// We assume for the moment that a and b share the same alphabet
	NAutomaton r = NewNAutomaton(a.n+b.n, a.na);
	//copie a
	for (i=0;i<a.n;i++)
	{
		//count the edges
		int nv = 0, rnv;
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			if (f != -1)
				nv++;
		}
		if (a.e[i].final)
			nv++; //add an edge to the other automaton
		rnv = nv;
		//alloc new edges
		r.e[i].a = (Transition *)malloc(sizeof(Transition)*nv);
		r.e[i].n = nv;
		//copy edges
		nv = 0;
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			if (f != -1)
			{
				r.e[i].a[nv].l = j;
				r.e[i].a[nv].e = f;
				nv++;
			}
		}
		if (a.e[i].final)
		{
			//add an espilon-transition to the initial state of the other automaton
			r.e[i].a[nv].l = -1;
			r.e[i].a[nv].e = a.n+b.i;
			nv++;
		}
		if (rnv != nv)
		{
			printf("Error : nv has not the right value !!!\n");
			exit(1);
		}
		r.e[i].final = 0;
		r.e[i].initial = (a.i == i);
	}
	//copy b
	for (i=0;i<b.n;i++)
	{
		//count the edges
		int nv = 0;
		for (j=0;j<b.na;j++)
		{
			if (b.e[i].f[j] != -1)
				nv++;
		}
		//alloc the new edges
		r.e[a.n+i].a = (Transition *)malloc(sizeof(Transition)*nv);
		r.e[a.n+i].n = nv;
		//copy the edges
		nv = 0;
		for (j=0;j<b.na;j++)
		{
			if (b.e[i].f[j] != -1)
			{
				r.e[a.n+i].a[nv].l = j;
				r.e[a.n+i].a[nv].e = a.n + b.e[i].f[j];
				nv++;
			}
		}
		r.e[a.n+i].final = b.e[i].final;
		r.e[a.n+i].initial = 0;
	}
	return r;
}

//convert a deterministic automaton to a non-deterministic one
void CopyDN(Automaton *a, NAutomaton *r, int verb)
{
    int i,j;
    for (i=0;i<a->n;i++)
	{
		//count the edges
		int nv = 0;
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
				nv++;
		}
		//alloc the new edges
		r->e[i].a = (Transition *)malloc(sizeof(Transition)*nv);
		r->e[i].n = nv;
		//copy the edges
		nv = 0;
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
			{
				r->e[i].a[nv].l = j;
				r->e[i].a[nv].e = a->e[i].f[j];
				nv++;
			}
		}
		r->e[i].final = a->e[i].final;
		r->e[i].initial = (a->i == i);
	}
}

//convert a deterministic automaton to a non-deterministic one
NAutomaton CopyN(Automaton a, int verb)
{
	NAutomaton r = NewNAutomaton(a.n, a.na);
	CopyDN(&a, &r, verb);
	return r;
}

//change the alphabet of the automaton
NAutomaton Proj (Automaton a, Dict d, int verb)
{
	//compute the size of the new alphabet
	int nv = 0;
	int i,j;
	for (i=0;i<d.n;i++)
	{
		if (d.e[i] >= nv)
			nv = d.e[i]+1;
	}
	//
	NAutomaton r = NewNAutomaton(a.n, nv);
	for (i=0;i<a.n;i++)
	{
		//count the edges
		nv = 0;
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] != -1 && d.e[j] != -1)
				nv++;
		}
		//alloc new edges
		r.e[i].a = (Transition *)malloc(sizeof(Transition)*nv);
		r.e[i].n = nv;
		//copy edges
		nv = 0;
		for (j=0;j<a.na;j++)
		{
			if (a.e[i].f[j] != -1 && d.e[j] != -1)
			{
				r.e[i].a[nv].l = d.e[j];
				r.e[i].a[nv].e = a.e[i].f[j];
				nv++;
			}
		}
		r.e[i].final = a.e[i].final;
		r.e[i].initial = (a.i == i);
	}
	return r;
}

//Add to e all states reached by an epsilon-transition from state i
void EpsilonParcours (NAutomaton a, uint i, States2 e)
{
	if (!hasStates2(e, i))
	{
		addState(&e, i);
		uint j;
		for (j=0;j<a.e[i].n;j++)
		{
			if (a.e[i].a[j].l == -1) //it is an epsilon-transition
			{
				EpsilonParcours(a, a.e[i].a[j].e, e);
			}
		}
	}
}

//compute the epsilon-closure of e (result in ec)
void EpsilonCloture (NAutomaton a, States2 e, States2 ec)
{
	int j;
	initStates2(ec);
	for (j=0;j<a.n;j++)
	{
		if (hasStates2(e, j))
		{
			EpsilonParcours(a, j, ec);
		}
	}
}

//Determinize a non-deterministic automaton
Automaton DeterminizeN (NAutomaton a, int sink_state, int verb)
{
	if (verb)
		printf("allocation...\n");
	
	Automaton r = NewAutomaton(a.n, a.na);
	
	if (a.n == 0)
		return r;
	
	if (verb >= 20)
		printf("allocates the hash table...\n");
	
	AllocHash();
	
	if (verb >= 20)
		printf("allocates states...\n");
	
	int i,j,k,u;
	ListStates2 l = NewListStates2(1, 1024);
	States2* e = (States2*)malloc(sizeof(States2)*a.na);
	for (i=0;i<a.na;i++)
	{
		e[i] = NewStates2(a.n);
	}
	
	States2 ec = NewStates2(a.n);
	
	if (verb >= 20)
		printf("allocates the first state...\n");
	
	//initialize the first state
	r.i = 0;
	l.e[0] = NewStates2(a.n);
	initStates2(l.e[0]);
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].initial)
			addState(&l.e[0], i);
	}
	l.n = 0;
	addStates2(&l, l.e[0], NULL); //add to the hash table
	l.n++;
	
	if (verb)
		printf("way...\n");
	
	for (i=0;i<l.n;i++)
	{ //browse states of the new automaton
		
		if (verb >= 20)
		{
			printf("state %d : ", i);
			printStates2(l.e[i]);
		}
		
		r.e[i].final = 0;
		for (j=0;j<a.na;j++)
		{
			initStates2(e[j]);
		}
		//compute the closure by epsilon-transition of l.e[i]
		EpsilonCloture(a, l.e[i], ec);
		//browse all edges leaving from states of ec
		for (j=0;j<a.n;j++)
		{ //browse states of a being in the current state
			if (hasStates2(ec, j))
			{
				r.e[i].final = r.e[i].final || a.e[j].final;
				for (u=0;u<a.e[j].n;u++)
				{ //browse edges leaving from state j of a
					if (a.e[j].a[u].l >= 0)
						addState(&e[a.e[j].a[u].l], a.e[j].a[u].e);
				}
			}
		}
		if (verb > 20)
			printf(" -> reached states :\n");
		for (j=0;j<a.na;j++)
		{ //browse reached states
			if (verb > 20)
			{
				printf("	");
				printStates2(e[j]);
			}
			if (sink_state || !isNullStates2(e[j]))
			{
				EpsilonCloture(a, e[j], ec);
				//determine if the state is new or not
				if (addStates2(&l, ec, &k))
				{
					ReallocListStates2(&l, l.n+1, 1);
					l.e[k] = copyStates2(ec);
					//add a state to the automaton
					if (l.n > r.n)
					{ //alloc the memory if needed
						ReallocAutomaton(&r, 2*l.n, 0);
					}
				}
				//add a edge labeled by j toward k in the new automaton
				r.e[i].f[j] = k;
			}else
			{
				r.e[i].f[j] = -1;
			}
		}
	}
	
	if (verb)
		printf("free...\n");
	
	//libère la mémoire
	ReallocAutomaton(&r, l.n, 0);
	
	//put to zero elements of the hash table
	for (i=0;i<l.n;i++)
	{
		FreeDict(&lhash[hash2(l.e[i])]);
	}
	
	FreeListStates2(&l);
	for (i=0;i<a.na;i++)
	{
		FreeStates2(e[i]);
	}
	free(e);
	//FreeHash(); //do not free memory in order to use it faster later
	return r;
}

//change the alphabet by duplicating edges if needed
//the result is assumed to be deterministic !!!!
Automaton Duplicate (Automaton a, InvertDict id, int na2, int verb)
{
	if (verb)
	{
		printf("NewAutomaton(%d, %d)\n", a.n, na2);
	}
	Automaton r = NewAutomaton(a.n, na2);

	if (verb)
	{
		printf("NewAutomaton(%d, %d) done.\n", a.n, na2);
	}
	
	int i,j,k;
	r.i = a.i;
	for (i=0;i<r.n;i++)
	{
		r.e[i].final = a.e[i].final;
		for (j=0;j<r.na;j++)
		{
			r.e[i].f[j] = -1;
		}
		for (j=0;j<a.na;j++)
		{
			for (k=0;k<id.d[j].n;k++)
			{
				r.e[i].f[id.d[j].e[k]] = a.e[i].f[j];
			}
		}
	}
	return r;
}

void ZeroComplete_ind(Automaton *a, int state, int *vu, int l0, int verb)
{
	if (verb)
		printf("state %d ..\n", state);
	vu[state] = 1;
	int i, e;
	for (i=0;i<a->na;i++)
	{
		e = a->e[state].f[i];
		if (e != -1 && e < a->n)
		{
			if (!vu[e])
				ZeroComplete_ind(a, e, vu, l0, verb);
			if (i == l0 && a->e[e].final)
				a->e[state].final = 1;
		}
	}
}

void ZeroComplete(Automaton *a, int l0, int verb)
{
	if (verb)
		printf("l0 = %d\n", l0);
	if (a->i == -1)
		return;
	int *vu = (int *)malloc(sizeof(int)*a->n); //list of seen states
	if (!vu)
	{
		printf("Out of memory !\n");
		exit(25);
	}
	int i;
	for (i=0;i<a->n;i++)
		vu[i] = 0;
	ZeroComplete_ind(a, a->i, vu, l0, verb);
	free(vu);
}

//same as ZeroComplete, but without induction
void ZeroComplete_(Automaton *a, int l0, int verb)
{
	if (verb)
		printf("l0 = %d\n", l0);
	if (a->i == -1)
		return;
	int *vu = (int *)malloc(sizeof(int)*a->n); //list of seen states
	if (!vu)
	{
		printf("Out of memory !\n");
		exit(25);
	}
	int i;
	for (i=0;i<a->n;i++)
		vu[i] = 0;
	int sp = log(a->n)+2; //size of stack
	int cp = 0; //current index
	int *se = (int*)malloc(sizeof(int)*sp); //stack
	//ZeroComplete_ind(a, a->i, vu, l0, verb);
	se[cp] = a->i;
	int state;
	while (cp >= 0)
	{
	    //pop
	    state = se[cp];
	    cp--;
	    if (verb)
		printf("state %d ..\n", state);
        vu[state] = 1;
        int i, e;
        for (i=0;i<a->na;i++)
        {
            e = a->e[state].f[i];
            if (e != -1 && e < a->n)
            {
                if (!vu[e])
                {
                    //ZeroComplete_ind(a, e, vu, l0, verb);
                    cp++;
                    if (cp >= sp)
                    {
                        //double the stack
                        sp = sp*2;
                        se = (int*)realloc(se, sizeof(int)*sp);
                    }
                    se[cp] = e;
                }
                if (i == l0 && a->e[e].final)
                    a->e[state].final = 1;
            }
        }
	}
	free(se); //free the stack
	free(vu);
}

Automaton ZeroComplete2 (Automaton *a, int l0, int sink_state, int verb)
{
	NAutomaton r = NewNAutomaton(a->n+1, a->na);
		
	int i,j,k;
	for (i=0;i<a->n;i++)
	{
		if (i == a->i)
			r.e[i].initial = 1;
		else
			r.e[i].initial = 0;
		r.e[i].final = a->e[i].final;
		r.e[i].n = 0;
		//count edges
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
				r.e[i].n++;
		}
		if (a->e[i].final)
			r.e[i].n++; //edge 0 added
		//alloc
		r.e[i].a = (Transition *)malloc(sizeof(Transition)*r.e[i].n);
		//fill
		k = 0;
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
			{
				r.e[i].a[k].e = a->e[i].f[j];
				r.e[i].a[k].l = j; 
				k++;
			}
		}
		if (a->e[i].final)
		{
			r.e[i].a[k].e = a->n; //add the edge to the state that recognize 0
			r.e[i].a[k].l = l0;
		}
	}
	r.e[a->n].n = 1;
	r.e[a->n].a = (Transition *)malloc(sizeof(Transition));
	r.e[a->n].a[0].e = a->n;
	r.e[a->n].a[0].l = l0;
	r.e[a->n].initial = 0;
	r.e[a->n].final = 1;
	
	return DeterminizeN(r, sink_state, 0);
}

Automaton EmptyAutomaton (int na)
{
    Automaton a = NewAutomaton(1, na);
    return a;
}

//Compute an automaton recognizing the language (l0*)L, where L is the language of a
Automaton ZeroInv (Automaton *a, int l0)
{
    if (a->i == -1)
    {
        return EmptyAutomaton(a->na);
	}
	NAutomaton r = NewNAutomaton(a->n+1, a->na);
	CopyDN(a, &r, 0);
	/*
	int i,j,k;
	for (i=0;i<a->n;i++)
	{
		if (i == a->i)
			r.e[i].initial = 1;
		else
			r.e[i].initial = 0;
		r.e[i].final = a->e[i].final;
		r.e[i].n = 0;
		//count the edges
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
				r.e[i].n++;
		}
		//alloc
		r.e[i].a = (Transition *)malloc(sizeof(Transition)*r.e[i].n);
		//fill
		k = 0;
		for (j=0;j<a->na;j++)
		{
			if (a->e[i].f[j] != -1)
			{
				r.e[i].a[k].e = a->e[i].f[j];
				r.e[i].a[k].l = j; 
				k++;
			}
		}
	}
	*/
	r.e[a->n].n = 2;
	r.e[a->n].a = (Transition *)malloc(sizeof(Transition)*2);
	r.e[a->n].a[0].e = a->n;
	r.e[a->n].a[0].l = l0;
	r.e[a->n].a[1].e = a->i;
	r.e[a->n].a[1].l = l0;
	r.e[a->n].initial = 1;
	r.e[a->n].final = 1;
	
	return DeterminizeN(r, 0, 0);
}

int countStates = 0;
int prune_inf_ind(Automaton a, int state)
{
	int i, f;
	int cycle = 0;
	a.e[state].final = 1; //mark the state as currently seen
	for (i=0;i<a.na;i++)
	{
		f = a.e[state].f[i];
		if (f == -1)
			continue;
		if (a.e[f].final == 1)
			cycle = 1; //the state is part of a cycle
		if (a.e[f].final == 0)
		{
			if (prune_inf_ind(a, f))
				cycle = 1; //the state permits to reach a cycle
		}
	}
	if (!cycle)
		a.e[state].final = 2; //indicate that we won't keep the state (but it has been seen)
	else
		countStates++; //count the states that we keep
	return cycle;
}

//remove every state from which there is no infinite path
Automaton prune_inf(Automaton a, int verb)
{
	int *l = (int *)malloc(sizeof(int)*a.n);
	if (!l)
	{
		printf("Out of memory !\n");
		exit(25);
	}
	
	//start by computing the list of states of a to keep
	int i;
	int *finaux = (int *)malloc(sizeof(int)*a.n);
	if (!finaux)
	{
		printf("Out of memory !\n");
		exit(13);
	}
	for (i=0;i<a.n;i++)
	{
		finaux[i] = a.e[i].final;
		a.e[i].final = 0; //states not seen
	}
	if (verb)
		printf("induction...\n");
	countStates = 0;
	if (a.i != -1)
		prune_inf_ind (a, a.i);
	
	if (verb)
	{
		printf("States counter = %d\n", countStates);
		printf("count...\n");
	}
	
	//count the states to keep
	int cpt = 0;
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final & 1)
		{ //new state to add
			l[i] = cpt;
			cpt++;
		}else
			l[i] = -1;
	}
	
	if (verb)
		printf("cpt = %d\n", cpt);
	
	//create the new automaton
	int j, f;
	Automaton r = NewAutomaton(cpt, a.na);
	for (i=0;i<a.n;i++)
	{
		if (l[i] == -1)
			continue;
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			r.e[l[i]].f[j] = -1;
			if (f == -1)
				continue;
			if (l[f] != -1)
			{
				r.e[l[i]].f[j] = l[f];
			}
		}
	}
	
	if (verb)
		printf("final states...\n");
	
	//put back final states as before
	for (i=0;i<a.n;i++)
	{
		a.e[i].final = finaux[i];
		if (l[i] != -1)
			r.e[l[i]].final = finaux[i];
	}
	
	//initial state
	if (a.i != -1)
		r.i = l[a.i];
	else
		r.i = -1;
	
	free(finaux);
	free(l);
	fflush(stdout);
	return r;
}

//remove every state from which there is no infinite path
//same as prune_inf, but without induction
/*
Automaton prune_inf2(Automaton a, int verb)
{
	int *l = (int *)malloc(sizeof(int)*a.n);
	if (!l)
	{
		printf("Out of memory !\n");
		exit(25);
	}
	
	//start by computing the list of states of a to keep
	int i;
	int *finaux = (int *)malloc(sizeof(int)*a.n);
	if (!finaux)
	{
		printf("Out of memory !\n");
		exit(13);
	}
	for (i=0;i<a.n;i++)
	{
		finaux[i] = a.e[i].final;
		a.e[i].final = 0; //states not seen
	}
	if (verb)
		printf("induction...\n");
	countStates = 0;
	if (a.i != -1)
	{
	    int sp = log(a.n)+2; //size of stack
	    int cp = 0; //current index
	    int *se = (int*)malloc(sizeof(int)*sp);
		//prune_inf_ind (a, a.i);
		se[cp] = a.i;
		int cycle;
		while (cp >= 0)
		{
		    //pop
		    state = se[cp];
		    cp--;
		    int i, f;
            cycle = 0;
            a.e[state].final = 1; //mark the state as currently seen
            for (i=0;i<a.na;i++)
            {
                f = a.e[state].f[i];
                if (f == -1)
                    continue;
                if (a.e[f].final == 1)
                    cycle = 1; //the state is part of a cycle
                if (a.e[f].final == 0)
                {
                    //if (prune_inf_ind(a, f))
                    //    cycle = 1; //the state permits to reach a cycle
                    cp++;
                    if (cp >= sp)
                    {
                        //double the stack
                        sp = sp*2;
                        se = (int*)realloc(sizeof(int)*sp);
                    }
                    se[cp] = f;
                    /////////////////////////////////////////////////////////////////////////////////
                    //////////////////////// TO FINISH !!!!!!!!!!!!!!!
                    /////////////////////////////////////////////////////////////////////////
                }
            }
            if (!cycle)
                a.e[state].final = 2; //indicate that we won't keep the state (but it has been seen)
            else
                countStates++; //count the states that we keep
            return cycle;
		}
	}
	
	if (verb)
	{
		printf("States counter = %d\n", countStates);
		printf("count...\n");
	}
	
	//count the states to keep
	int cpt = 0;
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final & 1)
		{ //new state to add
			l[i] = cpt;
			cpt++;
		}else
			l[i] = -1;
	}
	
	if (verb)
		printf("cpt = %d\n", cpt);
	
	//create the new automaton
	int j, f;
	Automaton r = NewAutomaton(cpt, a.na);
	for (i=0;i<a.n;i++)
	{
		if (l[i] == -1)
			continue;
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			r.e[l[i]].f[j] = -1;
			if (f == -1)
				continue;
			if (l[f] != -1)
			{
				r.e[l[i]].f[j] = l[f];
			}
		}
	}
	
	if (verb)
		printf("final states...\n");
	
	//put back final states as before
	for (i=0;i<a.n;i++)
	{
		a.e[i].final = finaux[i];
		if (l[i] != -1)
			r.e[l[i]].final = finaux[i];
	}
	
	//initial state
	if (a.i != -1)
		r.i = l[a.i];
	else
		r.i = -1;
	
	free(finaux);
	free(l);
	return r;
}
*/

//Compute the mirror, assuming it is deterministic
Automaton MirrorDet(Automaton a)
{
	Automaton r = NewAutomaton(a.n, a.na);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final)
			r.i = i;
		if (i == a.i)
			r.e[i].final = 1;
		else
			r.e[i].final = 0;
		for (j=0;j<a.na;j++)
		{
			r.e[i].f[j] = -1;
		}
	}
	int f;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			if (f != -1)
			{
				//printf("%d --%d--> %d\n", i, j, f);
				r.e[f].f[j] = i;
			}
		}
	}
	return r;
}

//Compute the mirror
NAutomaton Mirror(Automaton a)
{
	NAutomaton r = NewNAutomaton(a.n, a.na);
		
	int i,j;
	for (i=0;i<a.n;i++)
	{
		if (i == a.i)
			r.e[i].final = 1;
		else
			r.e[i].final = 0;
		r.e[i].initial = a.e[i].final;
		r.e[i].a = NULL;
		r.e[i].n = 0;
	}
		
	int f;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			if (f != -1)
			{
				//add an edge from f to i labeled by j
				r.e[f].n++;
				if (r.e[f].n == 1)
					r.e[f].a = (Transition *)malloc(sizeof(Transition));
				else
					r.e[f].a = (Transition *)realloc(r.e[f].a, sizeof(Transition)*r.e[f].n);
				r.e[f].a[r.e[f].n-1].l = j;
				r.e[f].a[r.e[f].n-1].e = i;
			}
		}
	}
	return r;
}

int count2;
void StronglyConnectedComponents_ind(Automaton a, int state, int *pile, int *m, int *res)
{
	int j,f,c;
	pile[countStates] = state;
	m[state] = countStates;
	c = countStates;
	a.e[state].final |= 2; //mark the state as seen
	countStates++;
	for (j=0;j<a.na;j++)
	{
		f = a.e[state].f[j];
		if (f == -1)
			continue;
		if (!(a.e[f].final & 2))
		{
			StronglyConnectedComponents_ind(a, f, pile, m, res);
			m[state] = min(m[state], m[f]);
		}else if (res[f] == -1)
		{
			m[state] = min(m[state], m[f]);
		}
	}
	if (m[state] == c)
	{ //we have a strongly connected component
	    //pops the component
		do
		{
			countStates--;
			res[pile[countStates]] = count2;
		}while(pile[countStates] != state);
		count2++;
	}
}

//Tarjan's algorithm
int StronglyConnectedComponents (Automaton a, int *res)
{
	int *m = (int *)malloc(sizeof(int)*a.n);
	int *pile = (int *)malloc(sizeof(int)*a.n);
	int i;
	for (i=0;i<a.n;i++)
	{
		res[i] = -1;
	}
	countStates = 0; //count the states added to the stack
	count2 = 0; //count the strongly connected components
	for (i=0;i<a.n;i++)
	{
		if (res[i] == -1)
			StronglyConnectedComponents_ind(a, i, pile, m, res);
	}
	//put back final states
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	free(pile);
	free(m);
	return count2;
}

//Tarjan's algorithm
//same as StronglyConnectedComponents, but without induction
int StronglyConnectedComponents2 (Automaton a, int *res)
{
	int *m = (int *)malloc(sizeof(int)*a.n);
	int *pile = (int *)malloc(sizeof(int)*a.n);
	int i, j,f,c, state;
	int count2;
	int sp = log(a.n)+2;
    int *se = (int*)malloc(sizeof(int)*sp);
    int *sj = (int*)malloc(sizeof(int)*sp);
    int *sc = (int*)malloc(sizeof(int)*sp);
    int cp = 0;
	for (i=0;i<a.n;i++)
	{
		res[i] = -1;
	}
	countStates = 0; //count the states added to the stack
	count2 = 0; //count the strongly connected components
	for (i=0;i<a.n;i++)
	{
		if (res[i] == -1)
		{
		    int cp = 0;
		    //StronglyConnectedComponents_ind(a, i, pile, m, res);
		    state = i;
start:		    
            pile[countStates] = state;
            m[state] = countStates;
            c = countStates;
            a.e[state].final |= 2; //mark the state as seen
            countStates++;
            //for (j=0;j<a.na;j++)
            j = 0;
            while(1)
            {
                if (j >= a.na)
                    break;
                f = a.e[state].f[j];
                if (f == -1)
                    continue;
                if (!(a.e[f].final & 2))
                {
                    //StronglyConnectedComponents_ind(a, f, pile, m, res);
                    //put current data in the stack
                    se[cp] = f;
                    sc[cp] = c;
                    sj[cp] = j;
                    cp++;
                    if (cp >= sp)
                    {
                        //double the stack
                        sp = sp*2;
                        se = (int*)realloc(se, sizeof(int)*sp);
                    }
                    state = f;
                    goto start;
                    //m[state] = min(m[state], m[f]);
                }else if (res[f] == -1)
                {
                    m[state] = min(m[state], m[f]);
                }
middle:
                j++;
            }
            if (m[state] == c)
            { //we have a strongly connected component
                //pops the component
                do
                {
                    countStates--;
                    res[pile[countStates]] = count2;
                }while(pile[countStates] != state);
                count2++;
            }
            if (cp > 0)
            {
                //pop
                cp--;
                j = sj[cp];
                c = sc[cp];
                state = se[cp];
                goto middle;
            }
            free(se);
		}
	}
	//put back final states
	for (i=0;i<a.n;i++)
	{
		a.e[i].final &= 1;
	}
	free(pile);
	free(m);
	return count2;
}

//determine reachable and co-reachable states
void prune_ind(Automaton a, int *l, InvertDict id, int state)
{
	//printf("prune_ind %d...\n", state);
	int i, j, f;
	a.e[state].final |= 2; //mark that this state is currently seen
	for (i=0;i<a.na;i++)
	{
		f = a.e[state].f[i];
		if (f == -1)
			continue;
		if (!(a.e[f].final & 2))
		{ //the state has not been seen
			prune_ind(a, l, id, f);
		}
		if ((a.e[f].final & 4) && !(a.e[state].final & 4))
		{ //we get to a co-final state that is not yet marked as co-final
		    //propagate the information to the strongly connected component
			for (j=0;j<id.d[l[state]].n;j++)
			{
				a.e[id.d[l[state]].e[j]].final |= 4;
			}
		}
	}
}

//remove every non-reachable and non-co-reachable states
//
// not really efficient : to improve !!!!!!!!!!!!!!!!!
//
Automaton prune(Automaton a, int verb)
{
	int i,j,f;
	
	//determine reachable and co-reachable states
	int *l = (int *)malloc(sizeof(int)*a.n);
	if (!l)
	{
		printf("Out of memory !\n");
		exit(15);
	}
	int ncc = StronglyConnectedComponents(a, l);
	if (verb)
	{
		printf("%d components : [", ncc);
		for (i=0;i<a.n;i++)
		{
			printf(" %d", l[i]);
		}
		printf(" ]\n");
	}
	InvertDict id = NewInvertDict(ncc);
	for (i=0;i<ncc;i++)
	{
		id.d[i] = NewDict(0);
	}
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final)
			a.e[i].final = 1;
		dictAdd(&id.d[l[i]], i);
	}
	if (verb)
		printInvertDict(id);
	//propagate final states to strongly connected components
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final & 1)
		{ //the state i is final and co-reachable but not already marked as co-reachable
			for (j=0;j<id.d[l[i]].n;j++)
			{
				a.e[id.d[l[i]].e[j]].final |= 4;
				if (verb)
					printf("%d co-acc\n", id.d[l[i]].e[j]);
			}
		}
	}
	//
	if (verb)
		printf("rec...\n");
	if (a.i != -1)
		prune_ind(a, l, id, a.i);
	
	//count the states to keep
	int cpt = 0;
	for (i=0;i<a.n;i++)
	{
		if ((a.e[i].final & 2) && (a.e[i].final & 4))
		{ //new state to add
			l[i] = cpt;
			cpt++;
		}else
			l[i] = -1;
	}
	
	if (verb)
	{
		printf("l : [");
		for (i=0;i<a.n;i++)
		{
			printf(" %d(%d)", l[i], a.e[i].final);
		}
		printf(" ]\n");
		
		printf("create the new automaton %d %d...\n", cpt, a.na);
	}
	//create the new automaton
	Automaton r = NewAutomaton(cpt, a.na);
	for (i=0;i<a.n;i++)
	{
		if (l[i] == -1)
		{
			if (verb)
				printf("pass %d\n", i);
			continue;
		}
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			r.e[l[i]].f[j] = -1;
			if (f == -1)
				continue;
			if (l[f] != -1)
			{
				r.e[l[i]].f[j] = l[f];
			}
		}
	}
	
	//put back the final states of a
	if (verb)
	{
		printf("deleted states : [");
		fflush(stdout);
	}
	for (i=0;i<a.n;i++)
	{
		if (verb)
		{
			if (l[i] == -1)
			{
				printf(" %d(", i);
				if (!(a.e[i].final & 2))
					printf(" non-acc");
				if (!(a.e[i].final & 4))
					printf(" non-co-acc");
				printf(" )");
			}
		}
		a.e[i].final &= 1;
		if (l[i] != -1)
			r.e[l[i]].final = a.e[i].final;
	}
	if (verb)
		printf(" ]\n");
	
	//initial state
	if (a.i != -1)
		r.i = l[a.i];
	else
		r.i = -1;
	
	FreeInvertDict(id);
	free(l);
	return r;
}

int AccCoAccRec (Automaton *a, int *coa, int e)
{
	if (coa[e] == 2)
	{
		int i, f;
		int coacc = a->e[e].final;
		coa[e] = 0; //indicate that the state has been seen
		for (i=0;i<a->na;i++)
		{
			f = a->e[e].f[i];
			if (f != -1)
				if (AccCoAccRec(a, coa, f))
					coacc = 1;
		}
		if (coacc)
			coa[e] = 1;
		return coacc;
	}else
		return (coa[e] == 1);
}

//determine the reachable and co-reachable states
// 0 : non co-reachable but reachable
// 1 : co-reachable and reachable
// 2 : non-reachable (but we don't know the co-reachability)
void AccCoAcc(Automaton *a, int *coa)
{
	int i;
	for (i=0;i<a->n;i++)
	{
		coa[i] = 2; //indicate states not seen yet
	}
	if (a->i != -1)
		AccCoAccRec(a, coa, a->i);
}

int CoAccRec (Automaton *a, int *coa, int e)
{
	if (coa[e] == 2)
	{
		int i, f;
		int coacc = a->e[e].final;
		coa[e] = 0; //indicate that the state has been seen
		for (i=0;i<a->na;i++)
		{
			f = a->e[e].f[i];
			if (f != -1)
				if (CoAccRec(a, coa, f))
					coacc = 1;
		}
		if (coacc)
			coa[e] = 1;
		return coacc;
	}else
		return (coa[e] == 1);
}

//determine the co-reachable states
// 0 : non co-reachable
// 1 : reachable
void CoAcc (Automaton *a, int *coa)
{
	int i;
	for (i=0;i<a->n;i++)
	{
		coa[i] = 2; //indicate states non seen yet
	}
	if (a->i != -1)
		CoAccRec(a, coa, a->i);
	for (i=0;i<a->n;i++)
	{
		if (coa[i] == 2)
			CoAccRec(a, coa, i);
	}
}

//determine reachable states
void pruneI_ind(Automaton a, int state)
{
	int i, f;
	a.e[state].final |= 2; //mark that the state is currently seen
	for (i=0;i<a.na;i++)
	{
		f = a.e[state].f[i];
		if (f == -1)
			continue;
		if (!(a.e[f].final & 2))
		{ //the state has not been seen yet
			pruneI_ind(a, f);
		}
	}
}

//remove every non-reachable states
Automaton pruneI(Automaton a, int verb)
{

	int i,j,f;
	//determine reachable states
	if (a.i != -1)
		pruneI_ind(a, a.i);

	int *l = (int *)malloc(sizeof(int)*a.n);
	if (!l)
	{
		printf("Out of memory !\n");
		exit(15);
	}

	//count the states to keep
	int cpt = 0;
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final & 2)
		{ //new state to add
			l[i] = cpt;
			cpt++;
		}else
			l[i] = -1;
	}
	
	//create the new automaton
	Automaton r = NewAutomaton(cpt, a.na);

	for (i=0;i<a.n;i++)
	{
		if (l[i] == -1)
			continue;
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			r.e[l[i]].f[j] = -1;
			if (f == -1)
				continue;
			if (l[f] != -1)
			{
				r.e[l[i]].f[j] = l[f];
			}
		}
	}

	//put back the final states of a
	if (verb)
	{
		printf("deleted states : [");
    	fflush(stdout);
	}
	for (i=0;i<a.n;i++)
	{
		if (verb)
		{
			if (l[i] == -1)
			{
				printf(" %d(", i);
				if (!(a.e[i].final & 2))
					printf(" not-acc");
				if (!(a.e[i].final & 4))
					printf(" not-co-acc");
				printf(" )");
			}
		}
		a.e[i].final &= 1;
		r.e[l[i]].final = a.e[i].final;
	}
	if (verb)
		printf(" ]\n");

	//initial state
	if (a.i != -1)
		r.i = l[a.i];
	else
		r.i = -1;

	free(l);

	return r;
}

Automaton SubAutomaton(Automaton a, Dict d, int verb)
{
	if (verb)
	{
		printf("dict = ");
		printDict(d);
	}
	Automaton r = NewAutomaton(d.n, a.na);
	int *l = (int *)malloc(sizeof(int)*a.n);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		l[i] = -1;
	}
	for (i=0;i<d.n;i++)
	{
		l[d.e[i]] = i;
	}
	
	if (verb)
	{
		printf("l = [");
		for (i=0;i<a.n;i++)
		{
			printf(" %d", l[i]);
		}
		printf(" ]\n");
	}
	
	for (i=0;i<r.n;i++)
	{
		for (j=0;j<r.na;j++)
		{
			r.e[i].f[j] = -1;
		}
	}
	for (i=0;i<a.n;i++)
	{
		if (l[i] != -1)
		{
			r.e[l[i]].final = a.e[i].final;
			for (j=0;j<a.na;j++)
			{
			
				if (a.e[i].f[j] != -1)
					r.e[l[i]].f[j] = l[a.e[i].f[j]];
				else
					r.e[l[i]].f[j] = -1;
			}
		}
	}
	r.i = -1;
	if (a.i != -1)
	{
		r.i = l[a.i];
	}
	free(l);
	return r;
}

//permut labels of edges
//l gives old indices from new ones
Automaton Permut (Automaton a, int *l, int na, int verb)
{
	if (verb)
	{
		int i;
		printf("l = [ ");
		for (i=0;i<na;i++)
		{
			printf("%d ", l[i]);
		}
		printf("]\n");
	}
	Automaton r = NewAutomaton(a.n, na);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<na;j++)
		{		
			if (l[j] != -1)
				r.e[i].f[j] = a.e[i].f[l[j]];
			else
				r.e[i].f[j] = -1;
		}
		r.e[i].final = a.e[i].final;
	}
	r.i = a.i;
	return r;
}

//permut labels of edges ON PLACE
//l gives old indices from new ones
void PermutOP (Automaton a, int *l, int na, int verb)
{
	if (verb)
	{
		int i;
		printf("l = [ ");
		for (i=0;i<na;i++)
		{
			printf("%d ", l[i]);
		}
		printf("]\n");
	}
	int *lf = (int*)malloc(sizeof(int)*a.na);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		//save the edges
		for (j=0;j<a.na;j++)
		{
			lf[j] = a.e[i].f[j];
			a.e[i].f[j] = -1;
		}
		//put the new ones
		for (j=0;j<na;j++)
		{		
			if (l[j] != -1)
				a.e[i].f[j] = lf[l[j]];
		}
	}
	free(lf);
}

/////////////////////// the following is an implementation of Hopcroft's algorithm minimization

typedef int Couple[2];

int *partition; //state --> index
int *partitioni; //index --> state
int *class; //class of each state
Couple *class_indices; //interval of indices of the class
int nclass = 0; //nb of classes
Dict **transitioni; //inverse of transitions of the automaton: state, letter --> list of states
int *L; //list of class for which a refinement is needed
int nL; //nb of elements of L
int *pt_visited_class; //first non already seen index in the class
int *visited_class; //list of classes just seen (used in split)
int *states; //states to browse

int global_n = 0;
void print_partition ()
{
	int i;
	printf("partition = [");
	for (i=0;i<global_n+1;i++)
	{
		printf(" %d", partition[i]);
	}
	printf(" ]\n");
	printf("partitioni = [");
	for (i=0;i<global_n+1;i++)
	{
		printf(" %d", partitioni[i]);
	}
	printf(" ]\n");
}

void print_classes ()
{
	//display the list of classes
	int l,h,i,j;
	for (i=0;i<nclass;i++)
	{
		printf("class %d : ", i);
		l = class_indices[i][0];
		h = class_indices[i][1];
		for (j=l;j<h;j++)
		{
			printf("%d ", partitioni[j]);
		}
		printf("\n");
	}
}

//swap states i and j
void swap (int i, int j)
{
	if (i == j)
		return;
	int k = partition[i];
	partition[i] = partition[j];
	partition[j] = k;
	partitioni[k] = j;
	partitioni[partition[i]] = i;
}

void split (int C, int a, int verb)
{
	//compute the preimage of C
	int i,j,l,h, e, p, lp, ep, cp;
	int nrc = 0; //number of classes encountered
	l = class_indices[C][0];
	h = class_indices[C][1];
	//copy the list of vertices to browse (in case of it would be modified during the browsing)
	for (i=l;i<h;i++)
	{ //browse class C
		states[i] = partitioni[i]; //state of index i
	}
	for (i=l;i<h;i++)
	{ //browse class C
		e = states[i]; //state of index i
		for (j=0;j<transitioni[e][a].n;j++)
		{ //browse inverse image of state e by letter a
			p = transitioni[e][a].e[j]; //parent
			cp = class[p]; //class of p
			if (!pt_visited_class[cp])
			{ //the class p has not been seen yet in this call of spilt
				if (verb)
					printf("new visited class : %d (%d parent of %d)\n", cp, p, e);
				visited_class[nrc] = cp;
				pt_visited_class[cp] = class_indices[cp][0]; //lowest indice of the class of p
				nrc++;
			}else
			{
				if (verb)
					printf("re-visited class : %d (%d parent of %d)\n", cp, p, e);
			}
			ep = pt_visited_class[cp]; //index of the element to permut with p
			if (ep > partition[p])
			{
				if (verb)
					printf("vertex %d already seen\n", p);
				continue; //we already saw the state p
			}
			ep = partitioni[ep]; //element to permut with p
			swap(ep, p);
			pt_visited_class[cp]++;
		}
	}
	
	if (verb)
	{
		print_classes();
		printf("%d class encountered\n", nrc);
	}
	
	//create new classes
	for (i=0;i<nrc;i++)
	{
		cp = visited_class[i];
		
		/////only for verification : to be avoided
		//if (pt_visited_class[cp] > class_indices[cp][1])
		//{
		//	printf("***********\nError !!!\n***********\n");
		//}
		////
		
		l = class_indices[cp][0];
		h = class_indices[cp][1];
		j = pt_visited_class[cp];
		
		if (verb)
			printf("class %d : l = %d %d %d = h\n", cp, l, j, h);
		
		if (j < h)
		{ //we have to add a new class
			//choose the smallest class
			if (h - j > j - l)
			{ //we choose the left part
				class_indices[cp][0] = j; //the old class becomes the right part
				class_indices[nclass][0] = l;
				class_indices[nclass][1] = j;
			}else
			{ //we choose the right part
				class_indices[cp][1] = j; //the old class becomes the left part
				class_indices[nclass][0] = j;
				class_indices[nclass][1] = h;
			}
			//update classes of vertices
			for (j=class_indices[nclass][0];j<class_indices[nclass][1];j++)
			{
				class[partitioni[j]] = nclass;
			}
			L[nL] = nclass; //add the new class to L
			nL++;
			nclass++;
		}
		
		pt_visited_class[cp] = 0; //put back to 0
	}
}

//minimization by Hopcroft's Algorithm
//see "Around Hopcroft’s Algorithm", Manuel BACLET and Claire PAGETTI
Automaton Minimise(Automaton a, int verb)
{
	if (verb)
		global_n = a.n;
	//allocations
	transitioni = (Dict **)malloc(sizeof(Dict *)*(a.n+1)); //inverse of partitions
	partition = (int *)malloc(sizeof(int)*(a.n+1));
	partitioni = (int *)malloc(sizeof(int)*(a.n+1));
	class = (int *)malloc(sizeof(int)*(a.n+1)); //class of a state
	nclass = 0;
	class_indices = (Couple *)malloc(sizeof(Couple)*(a.n+1));
	visited_class = (int *)malloc(sizeof(int)*(a.n+1));
	pt_visited_class = (int *)malloc(sizeof(int)*(a.n+1));
	states = (int *)malloc(sizeof(int)*(a.n+1));
	L = (int *)malloc(sizeof(int)*(a.n+1));	 //list of classes for which a refinement is needed
	nL = 0;
	int i,j,f;
	//initialize
	for (i=0;i<a.n+1;i++)
	{
		partition[i] = i;
		partitioni[i] = i;
		pt_visited_class[i] = 0;
	}
	
	//initialize inverses of transitions
	for (i=0;i<a.n+1;i++)
	{
		transitioni[i] = (Dict *)malloc(sizeof(Dict)*a.na);
		for (j=0;j<a.na;j++)
		{
			transitioni[i][j].e = NULL;
			transitioni[i][j].n = 0;
		}
	}
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			f = a.e[i].f[j];
			if (f != -1)
			{
				dictAdd(&transitioni[f][j], i);
			}else
			{
				dictAdd(&transitioni[a.n][j], i); //sink state
			}
		}
	}
	for (j=0;j<a.na;j++)
	{
		dictAdd(&transitioni[a.n][j], a.n); //transitions of sink state
	}
	
	if (verb)
	{
		for (i=0;i<a.n+1;i++)
		{
			for (j=0;j<a.na;j++)
			{
				printf("transition i[%d][%d] = [", i, j);
				for (f=0;f<transitioni[i][j].n;f++)
				{
					printf(" %d", transitioni[i][j].e[f]);
				}
				printf(" ]\n");
			}
		}
	}
	
	//start by separating final and non-final states
	f = 0; //count the final states
	for (i=0;i<a.n;i++)
	{
		if (a.e[i].final)
		{
			class[i] = 0;
			swap(partitioni[f], i);
			f++;
		}else
			class[i] = 1;
	}
	class[a.n] = 1;
	//classe 0 : final states, classe 1 : the rest
	class_indices[0][0] = 0;
	class_indices[0][1] = f;
	class_indices[1][0] = f;
	class_indices[1][1] = a.n+1;
	visited_class[0] = 0;
	visited_class[1] = 0;
	nclass = 2;
	
	if (verb)
		print_partition();
	
	if (verb)
	{
		printf("Initial partition :\n");
		print_classes();
	}
	
	//choose the smallest class
	if (f <= (a.n+1)/2)
		L[0] = 0;
	else
		L[0] = 1;
	nL = 1;
	
	//algo
	int C; //current class
	while (nL)
	{
		//remove the first class from the list L
		nL--;
		C = L[nL];
		//partion according to this class
		for (j=0;j<a.na;j++)
		{
			if (verb)
				printf("split %d %d...\n", C, j);
			split(C, j, verb);
		}
	}
	
	if (verb)
	{
		printf("Final partition :\n");
		print_classes();
	}
	
	//create the new automaton
	int e;
	Automaton r = NewAutomaton(nclass, a.na);
	for (i=0;i<nclass;i++)
	{
		e = partitioni[class_indices[i][0]]; //a state of the class
		if (e >= a.n)
		{ //sink state
			for (j=0;j<a.na;j++)
				r.e[i].f[j] = -1;
			r.e[i].final = 0;
			continue;
		}
		for (j=0;j<a.na;j++)
		{
			if (a.e[e].f[j] != -1)
			{
				f = class[a.e[e].f[j]];
				r.e[i].f[j] = f;
			}else
				r.e[i].f[j] = -1;
		}
		r.e[i].final = a.e[e].final;
	}
	
	if (verb)
	{
		printf("a.i = %d", a.i);
		if (a.i != -1)
		{
			printf(" class %d", class[a.i]);
		}
		printf("\n");
	}
	
	if (a.i != -1)
		r.i = class[a.i];
	else
		r.i = -1;
	
	//remove the sink state if not present in the initial automaton
	i = class[a.n];
	if (class_indices[i][1] == class_indices[i][0]+1)
	{ //we have to remove the sink state
		if (verb)
			printf("removes the sink state  %d...\n", i);
		DeleteVertexOP(&r, i);
	}
	
	//free the memory
	for (i=0;i<a.n+1;i++)
	{
		for (j=0;j<a.na;j++)
		{
			if (transitioni[i][j].e != NULL)
				free(transitioni[i][j].e);
		}
		free(transitioni[i]);
	}
	free(transitioni);
	free(partition);
	free(partitioni);
	free(class);
	free(class_indices);
	free(visited_class);
	free(pt_visited_class);
	free(states);
	free(L);
	
	fflush(stdout);
	
	return r;
}

//////////////////////////////////////////////////////////////////////////////////////////////
// End of the implementation of the Hopcroft's algorithm
//////////////////////////////////////////////////////////////////////////////////////////////

void DeleteVertexOP(Automaton *a, int e)
{
	if (e < 0 || e >= a->n)
		printf("The states %d is not in the automaton !\n", e);
	int i,j,f;
	a->n--;
	if (!a->n)
	{
		free(a->e);
		a->e = NULL;
		return;
	}
	for (i=0;i<a->n;i++)
	{
		for (j=0;j<a->na;j++)
		{
			f = a->e[i+(i>=e)].f[j];
			if (f != e)
				a->e[i].f[j] = f-(f>=e);
			else
				a->e[i].f[j] = -1;
		}
		a->e[i].final = a->e[i+(i>=e)].final;
	}
	if (e == a->i)
		a->i = -1;
	else
		a->i = a->i - (a->i>=e);
}

Automaton DeleteVertex (Automaton a, int e)
{
	if (e < 0 || e >= a.n)
		printf("The state %d is not in the automaton !\n", e);
	Automaton r = NewAutomaton(a.n-1, a.na);
	int i,j,f;
	for (i=0;i<a.n-1;i++)
	{
		for (j=0;j<a.na;j++)
		{
			f = a.e[i+(i>=e)].f[j];
			if (f != e)
				r.e[i].f[j] = f-(f>=e);
			else
				r.e[i].f[j] = -1;
		}
		r.e[i].final = a.e[i+(i>=e)].final;
	}
	r.i = a.i - (a.i>=e);
	return r;
}

Automaton BiggerAlphabet (Automaton a, Dict d, int nna)
{
	if (d.n != a.na)
	{
		printf("BA Error : the dictionnary must be of the same size as the previous alphabet.\n");
		return NewAutomaton(0,0);
	}
	Automaton r = NewAutomaton(a.n, nna);
	initAutomaton(&r);
	int i,j;
	for (i=0;i<a.n;i++)
	{
		for (j=0;j<a.na;j++)
		{
			r.e[i].f[d.e[j]] = a.e[i].f[j];
		}
		r.e[i].final = a.e[i].final;
	}
	r.i = a.i;
	return r;
}

