#include<stdio.h>
int main(){
    int a,b,c,d,e;
    float percentage;

    printf("enter your marks of subject 1\n");
    scanf("%d",&a);

    printf("enter your marks of subject 2\n");
    scanf("%d",&b);

    printf("enter your marks of subject 3\n");
    scanf("%d",&c);

    printf("enter your marks of subject 4\n");
    scanf("%d",&d);

    printf("enter your marks of subject 5\n");
    scanf("%d",&e);

    if(a>100||b>100||c>100||d>100||e>100){
        printf("verification not completed\n Invailid marks\n");
    }
    else{
        printf("Marks verification completed\n");
    }

    if(a>=34){
        printf("pass in subject 1\n");
    }
    else{
        printf("Fail in subject 1\n");
    }
    if(b>=34){
        printf("pass in subject 2\n");
    }
    else{
        printf("Fail in subject 2\n");
    }
    if(c>=34){
        printf("pass in subject 3\n");
    }
    else{
        printf("Fail in subject 3\n");
    }
    if(d>=34){
        printf("pass in subject 4\n");
    }
    else{
        printf("Fail in subject 4\n");
    }
    if(e>=34){
        printf("pass in subject 5\n");
    }
    else{
        printf("Fail in subject 5\n");
    }
    percentage = ((a+b+c+d+e)/5);
    printf("Total Pecentage %f\n",percentage);

    if(percentage>33){
        printf("PASS,Congratulation");
    }
    else{
        printf("FAIL,try again");
    }
    return 0;
}