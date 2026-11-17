#include <windows.h>
#include <stdio.h>
#include <string.h>
typedef void (*derive_t)(const unsigned char*, const char*, unsigned char*);
typedef void (*final_t)(const unsigned char*, const char*, const char*, unsigned char*);
typedef void (*valid_t)(const unsigned char*, unsigned char*);
static void hex(const unsigned char*b,int n){for(int i=0;i<n;i++)printf("%02x",b[i]);printf("\n");}
int main(void){
  HMODULE h=LoadLibraryA("NotionUpdate.exe");
  derive_t der=(derive_t)GetProcAddress(h,"GhostNote_deriveSession");
  final_t fin=(final_t)GetProcAddress(h,"GhostNote_finalFlagDigest");
  valid_t val=(valid_t)GetProcAddress(h,"GhostNote_validationDigest");
  unsigned char secret[32]={0x7a,0x21,0xd8,0x94,0xb5,0xd7,0x04,0xca,0x1f,0x2a,0x49,0x80,0x86,0x4e,0x52,0xde,0x7f,0x95,0x8d,0xd3,0x9f,0x8c,0xd3,0x23,0x22,0xf7,0xc5,0x68,0x0f,0xd8,0xf4,0xbd};
  const char*host="sync-notes-service.cloud"; const char*prof="GNT-0926";
  unsigned char sess[32],o[32];
  memset(sess,0,32); der(secret,host,sess); printf("dll session  "); hex(sess,32);
  memset(o,0,32); val(secret,o); printf("dll valid(sec)"); hex(o,32);
  memset(o,0,32); val(sess,o); printf("dll valid(ses)"); hex(o,32);
  const char* order[2][2]={{host,prof},{prof,host}};
  for(int i=0;i<2;i++){memset(o,0,32); fin(sess,order[i][0],order[i][1],o);printf("dll final(ses,%s,%s) ",order[i][0],order[i][1]);hex(o,32);}
  for(int i=0;i<2;i++){memset(o,0,32); fin(secret,order[i][0],order[i][1],o);printf("dll final(sec,%s,%s) ",order[i][0],order[i][1]);hex(o,32);}
  return 0;
}
