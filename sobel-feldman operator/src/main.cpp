#include <iostream>
#include <cinttypes>
#include <cmath>
#include <cstdio>

#include <stb_image.h>
#include <stb_image_write.h>

using std::cout;
using std::endl;
using std::uint8_t;

class Matrix
{
public:
  int *data;
  int width;
  int height;
  
  Matrix(uint8_t *data, int width, int height)
  {
    int *d = new int[width * height];
    for(int i = 0; i < (width * height); i++)
      d[i] = (int) data[i];
    
    this->data = d;
    this->width = width;
    this->height = height;
  }
  
  Matrix(int *data, int width, int height)
  { 
    this->data = data;
    this->width = width;
    this->height = height;
  }

  void set(int w, int h, int value)
  {
    this->data[h * this->width + w] = value;
  }

  int get(int w, int h)
  {
    if(w >= this->width || w < 0 || h >= this->height || h < 0)
      return 0;
    return this->data[h * this->width + w];
  }

  Matrix convolute(Matrix kernel)
  {
    uint8_t *opt = new uint8_t[this->width * this->height];
    Matrix output(opt, this->width, this->height);

    for(int w = 0; w < this->width; w++)
      {
	for(int h = 0; h < this->height; h++)
	  {
	    int value =
	      kernel.get(0, 0) * this->get(w - 1, h - 1) +
	      kernel.get(0, 1) * this->get(w - 1, h - 0) +
	      kernel.get(1, 0) * this->get(w - 0, h - 1) +
	      kernel.get(1, 1) * this->get(w - 0, h - 0) +
	      kernel.get(0, 2) * this->get(w - 1, h + 1) +
	      kernel.get(1, 2) * this->get(w - 0, h + 1) +
	      kernel.get(2, 2) * this->get(w + 1, h + 1) +
	      kernel.get(2, 0) * this->get(w + 1, h - 1) +
	      kernel.get(2, 1) * this->get(w + 1, h - 0);
	    output.set(w, h, value);
	  }
      }

    return output;
  }
};

int main(int argc, char **argv)
{
  if(argc != 3)
    {
      cout << "[ERROR] Wrong number of arguments provided" << endl;
      cout << "[Usage] " << argv[0] << " input_file" << " output_file" << endl;
      return 1;
    }

  int width, height, components;
  uint8_t *data = stbi_load(argv[1], &width, &height, &components, 1);
  if (data == NULL)
    {
      cout << "[ERROR] Could not open " << argv[1] << endl;
      if (fopen(argv[1], "rb") == NULL)
	perror("[ERROR]");
      return 1;
    }

  cout << "[INFO] Input : " << argv[1] << endl;
  cout << "[INFO] Width : " << width << endl;
  cout << "[INFO] Height : " << height << endl;

  // output grayscale
  // int result = stbi_write_jpg(argv[2], width, height, 1, data, 0);
  Matrix grayscale(data, width, height);
  // {1, 0, -1, 2, 0, -2, 1, 0 , -1}
  // {47, 0, -47, 162, 0, -162, 47, 0, -47}
  int x_kernel[] =  ;
  // {1, 2, 1, 0, 0, 0, -1, -2, -1}
  // {47, 162, 47, 0, 0, 0, -47, -162, -47}
  int y_kernel[] = {47, 162, 47, 0, 0, 0, -47, -162, -47};

  Matrix sobel_x({1, 0, -1,
                  2, 0, -2,
                  1, 0 , -1}, 3, 3);
  Matrix sobel_y({1, 2, 1,
                  0, 0, 0,
                  -1, -2, -1}, 3, 3);

  Matrix Gx = grayscale.convolute(sobel_x);
  Matrix Gy = grayscale.convolute(sobel_y);
  
  double *magnitude = new double[width * height];
  double max_magnitude = 0;
  for(int i = 0; i < (width * height); i++)
    {
      double value = std::sqrt(Gx.data[i] * Gx.data[i] + Gy.data[i] * Gy.data[i]);
      if (value > max_magnitude)
	max_magnitude = value;
      magnitude[i] = value;
    }
  cout << "[INFO] Max magnitude : " << max_magnitude << endl;
  
  uint8_t *output = new uint8_t[width * height];
  for(int i = 0; i < (width * height); i++)
    {
      output[i] = (magnitude[i] / max_magnitude) * 255;
    }

  int success = stbi_write_jpg(argv[2], width, height, 1, edges_image, 0);
  if(!success)
    {
      cout << "[ERROR] Could not create file " << argv[2] << endl;
      if(fopen(argv[2], "wb") == NULL)
	perror("[ERROR]");
      return success;
    }
  cout << "[INFO] Output : " << argv[2] << endl;  
  return 0;
}
