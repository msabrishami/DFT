#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <queue>
#include <cstdlib>
#include <iostream>
#include <cstring>
#include <vector>
using namespace std;

#define MAXLINE 81               /* Input buffer size */
#define MAXNAME 31               /* File name size */

#define Upcase(x) ((isalpha(x) && islower(x))? toupper(x) : (x))
#define Lowcase(x) ((isalpha(x) && isupper(x))? tolower(x) : (x))

enum e_com {READ, PC, HELP, QUIT, LEV, SIM, FLR, FLR2, DFS, PFS, FDG};
enum e_state {EXEC, CKTLD};         /* Gstate values */
enum e_ntype {GATE, PI, FB, PO};    /* column 1 of circuit format */
enum e_gtype {IPT, BRCH, XOR, OR, NOR, NOT, NAND, AND, XNOR};  /* gate types */

struct cmdstruc {
   char name[MAXNAME];        /* command syntax */
   int (*fptr)(char *cp);             /* function pointer of the commands */
   enum e_state state;        /* execution state sequence */
};

typedef struct n_struc {
   unsigned indx;             /* node index(from 0 to NumOfLine - 1 */
   unsigned num;              /* line number(May be different from indx */
   enum e_gtype type;         /* gate type */
   unsigned fin;              /* number of fanins */
   unsigned fout;             /* number of fanouts */
   struct n_struc **unodes;   /* pointer to array of up nodes */
   struct n_struc **dnodes;   /* pointer to array of down nodes */
   int level;                 /* level of the gate output */
   bool node_value;
   unsigned fin_lev;
   unsigned long fault_node_value;
   int sa0;					//use for flr, flr2
   int sa1;					//use for flr, flr2
} NSTRUC;                     

/*----------------- Command definitions ----------------------------------*/
#define NUMFUNCS 11
int cread(char *cp), pc(char *cp), lev(char *cp), help(char *cp), quit(char *cp), sim(char *cp), flr(char *cp), flr2(char *cp), dfs(char *cp), pfs(char *cp), fdg(char *cp);
char *gname(int tp);
void allocate();
void clear();

struct cmdstruc command[NUMFUNCS] = {
   {"READ", cread, EXEC},
   {"PC", pc, CKTLD},
   {"HELP", help, EXEC},
   {"QUIT", quit, EXEC},
   {"LEV", lev, CKTLD},
   {"LOGICSIM", sim, CKTLD},
   {"FLR", flr, CKTLD},
   {"FLR2", flr2, CKTLD},
   {"DFS", dfs, CKTLD},
   {"PFS", pfs, CKTLD},
   {"FDG", fdg, CKTLD}
};

/*------------------------------------------------------------------------*/
enum e_state Gstate = EXEC;     /* global exectution sequence */
NSTRUC *Node;                   /* dynamic array of nodes */
NSTRUC **Pinput;                /* pointer to array of primary inputs */
NSTRUC **Poutput;               /* pointer to array of primary outputs */
int Nnodes;                     /* number of nodes */
int Npi;                        /* number of primary inputs */
int Npo;                        /* number of primary outputs */
int Done = 0;                   /* status bit to terminate program */
char namefile[MAXLINE];
vector< vector<NSTRUC*> > lev_array;
//int fault_list[2*MAXLINE];
/*------------------------------------------------------------------------*/

/*-----------------------------------------------------------------------*/
main() //make sure do read first
{
   enum e_com com;
   char cline[MAXLINE], wstr[MAXLINE], *cp, *cp2;
   int com_temp;

   while(!Done) {
      printf("\nCommand>");
      fgets(cline, MAXLINE, stdin); //receive command from keyboard
      if(sscanf(cline, "%s", wstr) != 1) continue;
      cp = wstr;
      while(*cp){
	   *cp= Upcase(*cp);
	   cp++;
      }
      cp = cline + strlen(wstr);
      com = READ;
      while(com < NUMFUNCS && strcmp(wstr, command[com].name)){
         com_temp = static_cast<int>(com);
         com_temp++;
         com = static_cast<e_com>(com_temp);
      }
      if(com < NUMFUNCS) {
         if(command[com].state <= Gstate) 
            (*command[com].fptr)(cp);
         else printf("Execution out of sequence!\n");
      }
      else system(cline);
   }
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int cread(char *cp)
{
   char buf[MAXLINE];
   int ntbl, *tbl, i, j, k, nd, tp, fo, fi, ni = 0, no = 0;
   FILE *fd;
   NSTRUC *np;

   sscanf(cp, "%s", buf);
   strcpy(namefile, buf);
   if((fd = fopen(buf,"r")) == NULL) {
      printf("File %s does not exist!\n", buf);
      return 0;
   }
   if(Gstate >= CKTLD) clear();
   Nnodes = Npi = Npo = ntbl = 0;
   while(fgets(buf, MAXLINE, fd) != NULL) {  //go through numbers of node
      if(sscanf(buf,"%d %d", &tp, &nd) == 2) {
         if(ntbl < nd) 
            ntbl = nd;
         Nnodes ++;
         if(tp == PI) Npi++;
         else if(tp == PO) Npo++;
      }
   }
   tbl = (int *) malloc(++ntbl * sizeof(int));

   fseek(fd, 0L, 0);
   i = 0;
   while(fgets(buf, MAXLINE, fd) != NULL) {
      if(sscanf(buf,"%d %d", &tp, &nd) == 2) tbl[nd] = i++; //total number
   }
   allocate();

   fseek(fd, 0L, 0);
   while(fscanf(fd, "%d %d", &tp, &nd) != EOF) {
      np = &Node[tbl[nd]];
      np->num = nd; //index
      if(tp == PI) Pinput[ni++] = np;
      else if(tp == PO) Poutput[no++] = np;
      switch(tp) {
         case PI:
         case PO:
         case GATE:
            fscanf(fd, "%d %d %d", &np->type, &np->fout, &np->fin);
            break;
         
         case FB:
            np->fin = 1;
            fscanf(fd, "%d %d", &np->type, &np->fout);
            break;

         default:
            printf("Unknown node type!\n");
            exit(-1);
         }
      np->unodes = (NSTRUC **) malloc(np->fin * sizeof(NSTRUC *));
      np->dnodes = (NSTRUC **) malloc(np->fout * sizeof(NSTRUC *));
      for(i = 0; i < np->fin; i++) {
         fscanf(fd, "%d", &nd);
         np->unodes[i] = &Node[tbl[nd]];
         }
      for(i = 0; i < np->fout; np->dnodes[i++] = NULL);
      }
   for(i = 0; i < Nnodes; i++) {
      for(j = 0; j < Node[i].fin; j++) {
         np = Node[i].unodes[j];
         k = 0;
         while(np->dnodes[k] != NULL) k++;
         np->dnodes[k] = &Node[i];  // next equals to myself
         }
      }
   fclose(fd);
   Gstate = CKTLD;
   printf("==> OK\n");
   return 0;
}


/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int pc(char *cp)
{
   int i, j;
   NSTRUC *np;
   
   printf(" Node   Type \tIn     \t\t\tOut    \n");
   printf("------ ------\t-------\t\t\t-------\n");
   for(i = 0; i<Nnodes; i++) {
      np = &Node[i];
      printf("\t\t\t\t\t");
      for(j = 0; j<np->fout; j++) printf("%d ",np->dnodes[j]->num);
      printf("\r%5d  %s\t", np->num, gname(np->type));
      for(j = 0; j<np->fin; j++) printf("%d ",np->unodes[j]->num);
      printf("\n");
   }
   printf("Primary inputs:  ");
   for(i = 0; i<Npi; i++) printf("%d ",Pinput[i]->num);
   printf("\n");
   printf("Primary outputs: ");
   for(i = 0; i<Npo; i++) printf("%d ",Poutput[i]->num);
   printf("\n\n");
   printf("Number of nodes = %d\n", Nnodes);
   printf("Number of primary inputs = %d\n", Npi);
   printf("Number of primary outputs = %d\n", Npo);
   return 0;
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int sim(char *cp){
	NSTRUC *np;
	int PI_num[Nnodes], PI_value[Nnodes], k=0, lev_temp=1, lev_max=0, i, j;
	char in_file[MAXLINE], out_file[MAXLINE];
	lev(cp);
	sscanf(cp, "%s %s", in_file, out_file);
	
	FILE *fp1, *fp2;
	
	fp1 = fopen(in_file, "r");
	if(!fp1)	printf("can't open file\n");
	while(fscanf(fp1, "%d,%d", &PI_num[k], &PI_value[k]) != EOF)
	{  for(i=0; i<Nnodes; i++){	
			np = &Node[i];
			if(np->num == PI_num[k]){
				np->node_value = PI_value[k];
				// if (PI_value[k] == 1)
				   // np->fault_node_value = -1;
				// else
				   // np->fault_node_value = 0; 
			}	

		}	k++;
	}
	fclose(fp1);

   for (int level_x=1;level_x<lev_array.size();level_x++){
      for (int level_num=0;level_num<lev_array[level_x].size();level_num++)
      {
         np=lev_array[level_x][level_num];
         	switch (np->type)
				{
					case 1:
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = np->unodes[j]->node_value;
									}
									break;
					case 2:
									np->node_value = 0;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)^(np->unodes[j]->node_value);
									}
									break;
					case 8:
									np->node_value = 0;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)^(np->unodes[j]->node_value);
									}
									np->node_value = ! np->node_value;
									break;				
					case 3:
									np->node_value = 0;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)|(np->unodes[j]->node_value);
									}
									break;
					case 4:
									np->node_value = 0;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)|(np->unodes[j]->node_value);
									}
									np->node_value = ! np->node_value;
									break;
					case 5:
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = ! np->unodes[j]->node_value;
									}
									break;
					case 6:
									np->node_value = 1;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)&(np->unodes[j]->node_value);
									}
									np->node_value = ! np->node_value;
									break;
					case 7:
									np->node_value = 1;
									for (j=0; j<(np->fin); j++)
									{
										np->node_value = (np->node_value)&(np->unodes[j]->node_value);
									}
									break;
					default:		printf("error\n");
				}
      }
   }
   lev_max = lev_array.size()-2;
	fp2 = fopen(out_file, "w");
	if(fp2 != NULL)
	{
		for(i=0; i<Npo; i++)
		{
			np = Poutput[i];
			fprintf(fp2, "%d,%d\n", np->num, np->node_value);
		}
	}   
	fclose(fp2);
	return 0;
}
/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int fdg(char *cp){
	int fault_num[56];
	int fault_value[56];
	int valid[56];
	int fault_count = 0;
	
	FILE *fp, *fp1, *fp2, *fp3, *fp4, *fp5, *fp6, *fp7, *fp8;
	
	fp = fopen("mini_project_fault_dictionary.csv", "w");
	if(!fp)	printf("can't open file\n");
	for(int i=1; i < 29; i++){
		fprintf(fp,",%d@%d,%d@%d", i,0,i,1);
	}
	fprintf(fp,"\n");
	
	fp1 = fopen("mini_out0.txt", "r");
	if(!fp1)	printf("can't open file\n");
	while(fscanf(fp1, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp1);
	fprintf(fp,"%d%d%d,", 0,0,0);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");

	fp2 = fopen("mini_out1.txt", "r");
	if(!fp2)	printf("can't open file\n");
	while(fscanf(fp2, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp2);
	fprintf(fp,"%d%d%d,", 0,0,1);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp3 = fopen("mini_out2.txt", "r");
	if(!fp3)	printf("can't open file\n");
	while(fscanf(fp3, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp3);
	fprintf(fp,"%d%d%d,", 0,1,0);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp4 = fopen("mini_out3.txt", "r");
	if(!fp4)	printf("can't open file\n");
	while(fscanf(fp4, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp4);
	fprintf(fp,"%d%d%d,", 0,1,1);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp5 = fopen("mini_out4.txt", "r");
	if(!fp5)	printf("can't open file\n");
	while(fscanf(fp5, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp5);
	fprintf(fp,"%d%d%d,", 1,0,0);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp6 = fopen("mini_out5.txt", "r");
	if(!fp6)	printf("can't open file\n");
	while(fscanf(fp6, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp6);
	fprintf(fp,"%d%d%d,", 1,0,1);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp7 = fopen("mini_out6.txt", "r");
	if(!fp7)	printf("can't open file\n");
	while(fscanf(fp7, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp7);
	fprintf(fp,"%d%d%d,", 1,1,0);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");
	
	fp8 = fopen("mini_out7.txt", "r");
	if(!fp8)	printf("can't open file\n");
	while(fscanf(fp8, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){
		fault_count++;
	}
	fclose(fp8);
	fprintf(fp,"%d%d%d,", 1,1,1);
	for(int i=0; i<56; i++)		valid[i] = 0;
	for(int i=0; i < fault_count; i++){
		if(fault_value[i] == 0)		valid[2*fault_num[i]-2] = 1;
		else						valid[2*fault_num[i]-1] = 1;
	}
	for(int i=0; i<56; i++){
		if(valid[i] == 1)	fprintf(fp,"X,");
		else 				fprintf(fp,",");
	}
	fault_count = 0;
	fprintf(fp,"\n");

	
	
	
	
	fclose(fp);
	return 0;
}


int lev(char *cp)
{
    queue<NSTRUC*> q;
    int i,j,max;
    NSTRUC *np;
    char *gname();
	char namefile_temp[MAXLINE];
    int level_max=0;

    level_max++;
    for(i=0;i<Nnodes;i++){
      np = &Node[i];
      if (np->fin == 0){
         np->level = 0;
         lev_array.resize(level_max);
         lev_array[0].push_back(np);
         q.push(np);
      }
      np->fin_lev = np->fin;
    }   

    while(!q.empty()){
         level_max++;
         lev_array.resize(level_max);
         int s = q.size();
         for (i=0;i<s;i++){
            int max = 0;
            NSTRUC *temp = q.front();
            q.pop();
            for(j = 0; j < temp->fout; j++) {
               np = temp->dnodes[j];
               np->fin_lev--;
               if (np->fin_lev == 0){
                  q.push(np); 
                  lev_array[level_max-1].push_back(np);                  
               }
            }
            for(j = 0; j < temp->fin; j++) {
               np = temp->unodes[j];
               if (max < np->level)
                  max = np->level;
            }
            if (temp->fin!=0)           
               temp->level = max +1;
         }
    }


    i=0;
    strcpy(namefile_temp, namefile);
	while (namefile_temp[i]!='.'){
       i++;
    }
    namefile_temp[i] = '\0';
    strcat(namefile_temp,"_level.txt\0\n"); 
    FILE *fp;
    fp = fopen(namefile_temp,"w+");
    for(i = 0; i<Nnodes; i++) {
      np = &Node[i];
      fprintf(fp,"%d,%d\n", np->num, np->level);
    }
    fclose(fp);
	memset(namefile_temp, '\0', sizeof(namefile_temp));
    return 0;
}

int flr(char *cp){
	vector< NSTRUC* > fault_list;
	NSTRUC *np;
	char namefile_temp[MAXLINE];

	sscanf(cp, "%s", namefile_temp);
	
	for(int i=0;i<Nnodes;i++){
		np = &Node[i];
		if (np->fin == 0 || gname(np->type)=="BRANCH"){
			np->sa0 = 1;
			np->sa1 = 1;
			fault_list.push_back(np);
		}
	}	
					
	FILE *fp;
    fp = fopen(namefile_temp,"w+");
    for(int i = 0; i<fault_list.size(); i++) {
		np = fault_list[i];
		if(np->sa0 == 1)	fprintf(fp,"%d@%d\n", np->num, 0);
		if(np->sa1 == 1)	fprintf(fp,"%d@%d\n", np->num, 1);
	}
    fclose(fp);
    return 0;
}

int flr2(char *cp){
	vector< NSTRUC* > fault_list;
	NSTRUC *np;
	char namefile_temp[MAXLINE];

	sscanf(cp, "%s", namefile_temp);

	
	for(int i=0;i<Nnodes;i++){
		np = &Node[i];
		if (np->fin == 0 || gname(np->type)=="BRANCH"){
			np->sa0 = 1;
			np->sa1 = 1;
			fault_list.push_back(np);
		}
	}	
	
 	for(int i=0; i<fault_list.size(); i++){
		for(int j=i+1; j<fault_list.size(); j++){
			if(fault_list[i]->dnodes[0]->num == fault_list[j]->dnodes[0]->num){
				if(gname(fault_list[j]->dnodes[0]->type) == "NAND" || gname(fault_list[j]->dnodes[0]->type) == "AND"){
					fault_list[j]->sa0 = 0;
				}
				if(gname(fault_list[j]->dnodes[0]->type) == "NOR" || gname(fault_list[j]->dnodes[0]->type) == "OR"){
					fault_list[j]->sa1 = 0;
				}					
			}
		}
	}		
		
	FILE *fp;
    fp = fopen(namefile_temp,"w+");
    for(int i = 0; i<fault_list.size(); i++) {
		np = fault_list[i];
		if(np->sa0 == 1)	fprintf(fp,"%d@%d\n", np->num, 0);
		if(np->sa1 == 1)	fprintf(fp,"%d@%d\n", np->num, 1);
	}
    fclose(fp);
    return 0;
}

int dfs(char *cp){
	vector< vector<int> > dev_list (Nnodes, vector<int>(2*Nnodes, 0));
	NSTRUC *np;
	int c_flag;
	vector<int> temp1 (2*Nnodes, 1);		//use for &
	vector<int> temp2 (2*Nnodes, 0);		//use for |
	vector<int> DEV_list (2*Nnodes, 0);		//final fault list
	char in_file[MAXLINE], out_file[MAXLINE];
	
	sim(cp); 						//logic simulation first(also lev)
	sscanf(cp, "%s %s", in_file, out_file);
	FILE *fp;
	
	for(int i=0; i<Nnodes; i++){
		np = &Node[i];
		if(np->node_value == 1)		dev_list[i][2*i]   = 1;
		else 						dev_list[i][2*i+1] = 1;
	}
		
	for (int level_x=1;level_x<lev_array.size();level_x++){
      for (int level_num=0;level_num<lev_array[level_x].size();level_num++){
			np = lev_array[level_x][level_num];
			switch (np->type){
				case 1:					
				case 5:
					for (int i=0; i<(np->fin); i++){
						for(int j=0; j<2*Nnodes; j++){	
							dev_list[np->indx][j] = dev_list[np->indx][j] | dev_list[np->unodes[i]->indx][j];
						}
					}
					break;
				case 2:
				case 8:
					for(int j=0; j<2*Nnodes; j++){
						dev_list[np->indx][j] = dev_list[np->indx][j] | (dev_list[np->unodes[0]->indx][j] ^ dev_list[np->unodes[1]->indx][j]);
					}
					break;
				case 3:
				case 4:
					for (int i=0; i<(np->fin); i++){
						for(int j=0; j<2*Nnodes; j++){	
							if(np->unodes[i]->node_value == 1){	
								temp1[j] = temp1[j] & dev_list[np->unodes[i]->indx][j];
								c_flag = 1;
							}
							else{	
								temp1[j] = temp1[j] & (! dev_list[np->unodes[i]->indx][j]);
								temp2[j] = temp2[j] | dev_list[np->unodes[i]->indx][j];
							}
						}
					}
					
					if (c_flag == 1){
						for(int i=0; i<2*Nnodes; i++){
							dev_list[np->indx][i] = dev_list[np->indx][i] | temp1[i];
							temp1[i] = 1;
							temp2[i] = 0;
							c_flag = 0;
						}
					}
					else{
						for(int i=0; i<2*Nnodes; i++){
							dev_list[np->indx][i] = dev_list[np->indx][i] | temp2[i];
							temp1[i] = 1;
							temp2[i] = 0;
						}
					}						
					break;
				case 6:
				case 7:
					for (int i=0; i<(np->fin); i++){
						for(int j=0; j<2*Nnodes; j++){	
							if(np->unodes[i]->node_value == 0){	
								temp1[j] = temp1[j] & dev_list[np->unodes[i]->indx][j];
								c_flag = 1;
							}
							else{	
								temp1[j] = temp1[j] & (! dev_list[np->unodes[i]->indx][j]);
								temp2[j] = temp2[j] | dev_list[np->unodes[i]->indx][j];
							}
						}
					}				
					
					if (c_flag == 1){
						for(int i=0; i<2*Nnodes; i++){
							dev_list[np->indx][i] = dev_list[np->indx][i] | temp1[i];
							temp1[i] = 1;
							temp2[i] = 0;
							c_flag = 0;
						}
					}
					else{
						for(int i=0; i<2*Nnodes; i++){
							dev_list[np->indx][i] = dev_list[np->indx][i] | temp2[i];
							temp1[i] = 1;
							temp2[i] = 0;
						}
					}						
					break;
				default:
					printf("error\n");
			}
		}
	}
	for(int i=0; i<Nnodes; i++){
		np = &Node[i];
		if(np->fout == 0){
			for(int j=0; j< 2*Nnodes; j++){
				DEV_list[j] = DEV_list[j] | dev_list[np->indx][j];
			}
		}
	}	
	
	fp = fopen(out_file, "w");
	if(fp != NULL)
	{
		for(int i=0; i<Nnodes; i++)
		{
			np = &Node[i];
			if(DEV_list[2*(np->indx)] == 1)			fprintf(fp, "%d@%d\n", np->num, 0);
			if(DEV_list[(2*(np->indx)+1)] == 1)		fprintf(fp, "%d@%d\n", np->num, 1);
		}
	}   
	fclose(fp);
	return 0;
}

int pfs(char *cp){

	NSTRUC *np;
	vector<unsigned long> pfs_list_am (Nnodes, -1);
	vector<unsigned long> pfs_list_om (Nnodes, 0);
	int PI_num[Nnodes], PI_value[Nnodes], PI_count=0;
	int fault_num[2*Nnodes], fault_value[2*Nnodes], fault_count=0;
	int n = 8*sizeof(unsigned long);
	char in_file1[MAXLINE], in_file2[MAXLINE], out_file[MAXLINE];
	unsigned long inter_fault_node_value;
    vector<int> good_value;
    vector<int> bad_value;
	
	vector<unsigned long> temp_am (Nnodes, -1);
	vector<unsigned long> temp_om (Nnodes, 0);
	
	lev(cp);
	
	sscanf(cp, "%s %s %s", in_file1, in_file2, out_file);
	FILE *fp1, *fp2, *fp3;
	
	fp1 = fopen(in_file1, "r");
	if(!fp1)	printf("can't open file\n");
	while(fscanf(fp1, "%d,%d", &PI_num[PI_count], &PI_value[PI_count]) != EOF){  
		PI_count++;
	}
	fclose(fp1);
	
	fp2 = fopen(in_file2, "r");
	if(!fp2)	printf("can't open file\n");
	while(fscanf(fp2, "%d@%d", &fault_num[fault_count], &fault_value[fault_count]) != EOF){  	
		fault_count++;
	}
	fclose(fp2);
	
	fp3 = fopen(out_file, "w");
	if(!fp3)	printf("can't open file\n");
	
	int counter = 0;
	while(counter < fault_count){
		for(int i=0; i<Nnodes; i++){			//initialize AND MASK & OR MASK for each parallel
			pfs_list_am[i] = -1;
			pfs_list_om[i] =  0;
		}
		for(int i=0; i<(n-1); i++){
			for(int j=0; j<Nnodes; j++){
				np = &Node[j];
				if((counter + i) < fault_count){
					if(fault_num[counter + i] == np->num){					
						// printf("Node number = %d____________\n", np->num);
						// printf("previous AM = %d\n", pfs_list_am[j]);
						// printf("previous OM = %d\n", pfs_list_om[j]);
						if(fault_value[counter + i] == 0)	
							pfs_list_am[j] = pfs_list_am[j] ^ ((unsigned long)1 << (i + 1));
						else
							pfs_list_om[j] = pfs_list_om[j] | ((unsigned long)1 << (i + 1));
						
						// int bin_am[n];													//good verify, keep it
						// int bin_om[n];
						// temp_am = pfs_list_am;
						// temp_om = pfs_list_om;
						// printf ("changed AM = %d\n", temp_am[np->indx]);
						// printf ("changed OM = %d\n", temp_om[np->indx]);
						// for(int q=0; q<n; q++){
							// bin_am[q] = temp_am[np->indx] % 2;
							// temp_am[np->indx] /= 2;
						// }
						// printf("binary  AM =");
						// for(int q=0; q<n; q++){
							// printf("%d", bin_am[n-q-1]);
						// }
						// printf("\n");
						
						// for(int q=0; q<n; q++){
							// bin_om[q] = temp_om[np->indx] % 2;
							// temp_om[np->indx] /= 2;
						// }
						// printf("binary  OM =");
						// for(int q=0; q<n; q++){
							// printf("%d", bin_om[n-q-1]);
						// }
						// printf("\n");
					}
				}
			}
		}
			

		for(int i=0; i<Npi; i++){			//initialize PI for each parallel
			np = Pinput[i];
			for(int j=0; j<PI_count; j++){
				if(np->num == PI_num[j]){
					if (PI_value[j] == 1)	np->fault_node_value = -1;
					else					np->fault_node_value =  0;
				}
			}
		}
		
		for (int level_x=0;level_x<lev_array.size();level_x++){
			for (int level_num=0;level_num<lev_array[level_x].size();level_num++){
				np=lev_array[level_x][level_num];
				switch (np->type){
					case 0:
							break;
					case 1:
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = np->unodes[j]->fault_node_value;
							}
							break;
					case 2:
							np->fault_node_value = 0;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)^(np->unodes[j]->fault_node_value);
							}
							break;
					case 8:
							np->fault_node_value = 0;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)^(np->unodes[j]->fault_node_value);
							}
							np->fault_node_value = ~ np->fault_node_value;
							break;		
					case 3:
							np->fault_node_value = 0;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)|(np->unodes[j]->fault_node_value);
							}
							break;
					case 4:
							np->fault_node_value = 0;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)|(np->unodes[j]->fault_node_value);
							}
							np->fault_node_value = ~ np->fault_node_value;
							break;
					case 5:
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = ~ np->unodes[j]->fault_node_value;
							}
							break;
					case 6:
							np->fault_node_value = -1;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)&(np->unodes[j]->fault_node_value);
							}
							np->fault_node_value = ~ np->fault_node_value;
							break;
					case 7:
							np->fault_node_value = -1;
							for (int j=0; j<(np->fin); j++){
								np->fault_node_value = (np->fault_node_value)&(np->unodes[j]->fault_node_value);
							}
							break;
					default:		printf("error\n");
				}
				np->fault_node_value = (np->fault_node_value & pfs_list_am[np->indx]) | pfs_list_om[np->indx];
		    }
	    }
						
		good_value.clear();
		for(int i=0; i<Npo; i++){
			np = Poutput[i];
			good_value.push_back(np->fault_node_value & 1);						
			np->fault_node_value = np->fault_node_value>>1;
		}
		
		for (int i=0;i<(n-1);i++){
			if((counter + i) < fault_count){
				bad_value.clear();
				for(int j=0; j<Npo; j++){
					np = Poutput[j];
					bad_value.push_back(np->fault_node_value & 1);
					np->fault_node_value = np->fault_node_value>>1;
						
				}					
				if (bad_value != good_value){
					fprintf(fp3, "%d@%d\n", fault_num[counter + i], fault_value[counter + i]);
				}
			}
		}			
		counter = counter + n - 1;			
	}  
	fclose(fp3);	
	return 0;
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int help(char *cp)
{
   printf("READ filename - ");
   printf("read in circuit file and creat all data structures\n");
   printf("PC - ");
   printf("print circuit information\n");
   printf("LEV - ");
   printf("print Levelization information\n");
   printf("SIM - ");
   printf("Logic simulation\n");
   printf("FLR - ");
   printf("Fault list reduction\n");
   printf("FLR2 - ");
   printf("Fault list reduction2\n\n");
   printf("DFS - ");
   printf("Deductive fault simulation\n");   
   printf("PFS - ");
   printf("Parallel fault simulation\n");   
   printf("HELP - ");
   printf("print this help information\n");
   printf("QUIT - ");
   printf("stop and exit\n");
   return 0;
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
int quit(char *cp)
{
   Done = 1;
   return 0;
}

/*======================================================================*/

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
void clear()
{
   int i;

   for(i = 0; i<Nnodes; i++) {
      free(Node[i].unodes);
      free(Node[i].dnodes);
   }
   free(Node);
   free(Pinput);
   free(Poutput);
   Gstate = EXEC;
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
void allocate()
{
   int i;

   Node = (NSTRUC *) malloc(Nnodes * sizeof(NSTRUC));
   Pinput = (NSTRUC **) malloc(Npi * sizeof(NSTRUC *));
   Poutput = (NSTRUC **) malloc(Npo * sizeof(NSTRUC *));
   for(i = 0; i<Nnodes; i++) {
      Node[i].indx = i;
      Node[i].fin = Node[i].fout = 0;
   }
}

/*-----------------------------------------------------------------------
-----------------------------------------------------------------------*/
char* gname(int tp)
{
   switch(tp) {
      case 0: return((char*)"PI");
      case 1: return((char*)"BRANCH");
      case 2: return((char*)"XOR");
      case 3: return((char*)"OR");
      case 4: return((char*)"NOR");
      case 5: return((char*)"NOT");
      case 6: return((char*)"NAND");
      case 7: return((char*)"AND");
	  case 8: return((char*)"XNOR");
   }
   return (char*)"error";
}
/*========================= End of program ============================*/
