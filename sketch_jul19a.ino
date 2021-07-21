

#define Melody 5
#define Chord 6

int notemap[12] = {261,277,293,311,330,349,370,392,415,440,466,493};

struct note
{
  int p;
  int t;
};

struct note notes[]={{57,4},{55,4},{57,4},{52,4},{48,4},{47,4},{48,4},{45,4},{48,8},{60,8},{59,8},{55,8},{57,4},{59,4},{60,4},{64,4},{60,4},{59,4},{55,4},{47,4},{48,8},{55,8},{57,16},{57,4},{55,4},{57,4},{59,4},{60,4},{59,4},{62,4},{59,4},{60,4},{59,4},{57,4},{55,4},{48,8},{47,8},{45,4},{47,4},{48,4},{52,4},{48,4},{52,4},{48,4},{47,4},{45,4},{43,4},{40,4},{43,4},{45,16}};

int no(int n)
{
  if(n/12-3>=0)
    return notemap[n%12]*(1<<(n/12-3));
   return notemap[n%12]/(1<<(3-n/12));
}

int i;
void setup()
{
  i=0;
  pinMode(Melody,OUTPUT);
  pinMode(Chord,OUTPUT);
}

void loop()
{
  tone(Melody,no(notes[i].p));
  delay(notes[i].t*50);
  if(++i>=sizeof(notes)/sizeof(struct note))
    i=0;
  noTone(Melody);
}
