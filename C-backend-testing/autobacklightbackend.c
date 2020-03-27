/*
 ============================================================================
 Name        : autobacklightbackend.c
 Author      : 
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <string.h>
#include <errno.h>
#include <math.h>
#include <stdlib.h>
#include <fcntl.h>
#include <linux/videodev2.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <unistd.h>

uint8_t *buffer;

int strtoi (char *str){
    int num=0;
    int len = (int)(strchr(str, '\n')-str);

    int i;
    for ( i = 0; i < len; i++)
    {
       num=num+((int)str[i]-48)*(int)pow(10, len-i-1);
    }
    return num;
    
}
static int xioctl(int fd, int request, void *arg)
{
        int r;

        do r = ioctl (fd, request, arg);
        while (-1 == r && EINTR == errno);

        return r;
}
char *itostr(int i , int *h)
{
    int len=0, tmp=i;
    while(tmp>=1){
        tmp/=10;
        len++;
    }
    *h=len;
    
    char *str = (char*)calloc(len+1, sizeof(char));
    int j;
    tmp=i;
    for(j=len-1 ; j>=0 ; j--)
    {
        
        str[j]=(char)(tmp%10+'0');
        
        tmp=tmp/10;
    }  
    str[len]='\n';
  
    return str;
}
int setup_format(int fd)
{

        struct v4l2_format fmt = {0};
        fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        fmt.fmt.pix.width = 176;
        fmt.fmt.pix.height = 144;
        //fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_BGR24;
        //fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_GREY;
        fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_MJPEG;
        fmt.fmt.pix.field = V4L2_FIELD_NONE;

        if (-1 == xioctl(fd, VIDIOC_S_FMT, &fmt))
        {
            perror("Setting Pixel Format");
            return 1;
        }
        return 0;
}

int init_mmap(int fd)
{
    struct v4l2_requestbuffers req = {0};
    req.count = 1;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_MMAP;

    if (-1 == xioctl(fd, VIDIOC_REQBUFS, &req))
    {
        perror("Requesting Buffer");
        return 1;
    }

    struct v4l2_buffer buf = {0};
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;
    buf.index = 0;
    if(-1 == xioctl(fd, VIDIOC_QUERYBUF, &buf))
    {
        perror("Querying Buffer");
        return 1;
    }

    buffer = mmap (NULL, buf.length, PROT_READ | PROT_WRITE, MAP_SHARED, fd, buf.m.offset);


    return 0;
}

int capture_image(int fd)
{
    struct v4l2_buffer buf = {0};
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;
    buf.index = 0;
    if(-1 == xioctl(fd, VIDIOC_QBUF, &buf))
    {
        perror("Query Buffer");
        return 1;
    }

    if(-1 == xioctl(fd, VIDIOC_STREAMON, &buf.type))
    {
        perror("Start Capture");
        return 1;
    }

    fd_set fds;
    FD_ZERO(&fds);
    FD_SET(fd, &fds);
    struct timeval tv = {0};
    tv.tv_sec = 2;
    int r = select(fd+1, &fds, NULL, NULL, &tv);
    if(-1 == r)
    {
        perror("Waiting for Frame");
        return 1;
    }

    if(-1 == xioctl(fd, VIDIOC_DQBUF, &buf))
    {
        perror("Retrieving Frame");
        return 1;
    }

    if(-1 == xioctl(fd, VIDIOC_STREAMOFF, &buf.type))
    {
        perror("Start Capture");
        return 1;
    }

    return 0;
}

int main(int argc, char *argv[])
{
if(argc==1){
    perror("No arguments provided");
    return 1;
}

if (geteuid()!=0)
{
perror("No root access");
return 0;
}
        int fd;

        fd = open("/dev/video0", O_RDWR);
        if (fd == -1)
        {
                perror("Opening video device");
                return 1;
        }


        if(init_mmap(fd))
            return 1;
        int i;
       if(capture_image(fd))
	{
	perror("Capturing image");
	return 1;
	}	

        close(fd);
	
        long sum=0;
        for (i=0 ; i<144*176 ; i++){
        	sum+=buffer[i];
        }

        sum/=(144*176);
        int light_level = sum-80;
        if (light_level<0)
        	light_level=0;

int fp;
        fp = open(argv[1], O_RDWR);
if(fp == -1)
{
perror("Error opening brightness file");
return 1;
}

char *buff = (char*)calloc(6, sizeof(char));
if(read(fp, buff, 6)<=0){
perror("Error reading file");
return 1;
}


int currLevel=0;
i=0;
currLevel=strtoi(buff);

  free(buff);      
char *bf;
 //printf("%i, %c", currLevel, 'c');
     fflush(stdout);
        
        int incr=0;
        if(light_level>currLevel/960){
        	incr=1;
        }
        else{
        	incr=-1;
        }
        int j;
  int multi=currLevel/960;
      // printf("%i\n", multi);
     //  printf("%i\n", light_level);
       fflush(stdout);
        while(multi!=light_level)
        {
            
            lseek(fp, 0, SEEK_SET);
            
        	multi+=incr;
            fflush(stdout);
		    bf=itostr(multi*960, &j);
            
		    if(write(fp, bf, j)<j){
                perror("error writing");
                return 1;
            }
          
            //fflush(fp);
            
            
        	usleep(2000);
            
        }
        close(fp);

        return 0;

}
