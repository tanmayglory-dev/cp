#include<stdio.h>
int main(){
    int a,b,c,d,e;

    printf("enter your marks of subject 1/n\n");
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
        printf("verification not completed\n pls enter vailid number");
    }
    else{
        printf("verification completed\n");
    }


    return 0;
}