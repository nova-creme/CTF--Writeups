#include <windows.h>
#include <stdio.h>
#include <string.h>

typedef void (*decode_t)(const char*, char*, int);
typedef void (*derive_t)(const unsigned char*, const char*, unsigned char*);
typedef void (*final_t)(const unsigned char*, const char*, const char*, unsigned char*);
typedef void (*valid_t)(const unsigned char*, unsigned char*);

static void hex(const unsigned char*b,int n){for(int i=0;i<n;i++)printf("%02x",b[i]);printf("\n");}

int main(void){
    HMODULE h = LoadLibraryA("NotionUpdate.exe");
    if(!h){ printf("load failed %lu\n", GetLastError()); return 1; }
    decode_t dec = (decode_t)GetProcAddress(h,"GhostNote_decodeServer");
    derive_t der = (derive_t)GetProcAddress(h,"GhostNote_deriveSession");
    final_t fin = (final_t)GetProcAddress(h,"GhostNote_finalFlagDigest");
    valid_t val = (valid_t)GetProcAddress(h,"GhostNote_validationDigest");
    printf("procs %p %p %p %p\n", dec, der, fin, val);

    char out[128]; memset(out,0,sizeof out);
    dec("DNYT7", out, 6);
    printf("decode DNYT7 -> '%s'\n", out);

    unsigned char key[32]; for(int i=0;i<32;i++) key[i]=(unsigned char)i;
    unsigned char d[32]; memset(d,0,32);
    der(key, "abc", d);
    printf("derive(zero..31,\"abc\") = "); hex(d,32);

    unsigned char f[32]; memset(f,0,32);
    fin(key, "abc", "def", f);
    printf("final(zero..31,abc,def)  = "); hex(f,32);

    unsigned char v[32]; memset(v,0,32);
    val(key, v);
    printf("valid(zero..31)          = "); hex(v,32);
    return 0;
}
