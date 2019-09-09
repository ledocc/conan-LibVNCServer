#include <rfb/rfb.h>
#include <rfb/keysym.h>

int main(int argc,char** argv)
{
    rfbScreenInfoPtr rfbScreen = rfbGetScreen(&argc,argv,300,300,8,3,24);
    return 0;
}
