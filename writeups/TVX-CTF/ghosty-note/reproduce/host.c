#include <windows.h>
#include <stdio.h>
#include <string.h>
typedef void (*decode_t)(const char*, char*, int);
typedef int (*host_t)(const char*, char*);
int main(void){
  HMODULE h=LoadLibraryA("NotionUpdate.exe");
  decode_t dec=(decode_t)GetProcAddress(h,"GhostNote_decodeServer");
  host_t host=(host_t)GetProcAddress(h,"GhostNote_extractHostLower");
  const char* enc[]={
   "40 44 44 0d 18 18 59 58 43 5e 58 59 1a 56 44 44 52 43 44 1a 54 53 59 19 54 58 5a 0d 0e 03 03 04 18 42 47 53 56 43 52 37",
   "40 44 44 0d 18 18 64 6e 79 74 1a 79 78 63 72 64 1a 64 72 65 61 7e 74 72 19 74 7b 78 62 73 0d 0f 03 03 04 18 56 47 5e 18 41 05 37",
   "40 44 44 0d 18 18 59 58 43 52 44 1a 52 53 50 52 1a 54 56 54 5f 52 19 59 52 43 0d 03 03 04 18 44 4e 59 54 37"};
  for(int i=0;i<3;i++){
    char encbuf[256]; int n=0; const char*p=enc[i];
    while(*p){ if(*p==' '){p++;continue;} unsigned v; sscanf(p,"%2x",&v); encbuf[n++]=(char)v; p+=2; }
    encbuf[n]=0;
    char url[256]={0}, hostbuf[256]={0};
    dec(encbuf,url,n);
    int r=host(url,hostbuf);
    printf("url=[%s] ret=%d host=[%s]\n",url,r,hostbuf);
  }
  return 0;
}
