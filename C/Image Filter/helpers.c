#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avg; //  temp avg variable

    // looping over each row
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //  calculate the average
            avg = (int) round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);

            //  assign this average as the new RGB values
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //  image is an array that only contains the rgb pixels
    //  we loop over each pixel, we store the mirrored pixel opposite it in a temp variable
    //  then we set the opposite pixel's value equal to the current pixel and the current pixel's value equal to the temp pixel

    RGBTRIPLE temp; //  temp RGB variable

    //  looping over each row
    for (int i = 0; i < height; i++)
    {
        //  looping over each column
        //  the width / 2 ensures we only access half the image
        for (int j = 0; j < width / 2; j++)
        {
            // assigning opposite pixel to temp pixel
            temp.rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            temp.rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            temp.rgbtRed = image[i][width - 1 - j].rgbtRed;

            // assigning current pixel to opposite pixel
            image[i][width - 1 - j].rgbtBlue = image[i][j].rgbtBlue;
            image[i][width - 1 - j].rgbtGreen = image[i][j].rgbtGreen;
            image[i][width - 1 - j].rgbtRed = image[i][j].rgbtRed;

            //  assigning temp pixel to current pixel
            image[i][j].rgbtBlue = temp.rgbtBlue;
            image[i][j].rgbtGreen = temp.rgbtGreen;
            image[i][j].rgbtRed = temp.rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //  temp variables
    int sumR;
    int sumG;
    int sumB;
    int counter;
    int avgR;
    int avgG;
    int avgB;

    // temp copied array
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j] = image[i][j];
        }
    }

    //  looping over each row of copied array
    for (int i = 0; i < height; i++)
    { //  looping over each column of copied array
        for (int j = 0; j < width; j++)
        {
            sumR = 0; //  temp avg variable
            sumG = 0;
            sumB = 0;
            counter = 0;

            //  for each pixel check if the surrounding pixels exist
            for (int r = -1; r <= 1; r++)
            {
                for (int c = -1; c <= 1; c++)
                {
                    if (0 <= (i + r) && (i + r) < height && 0 <= (j + c) && (j + c) < width)
                    {
                        sumR += temp[i + r][j + c].rgbtRed;
                        sumG += temp[i + r][j + c].rgbtGreen;
                        sumB += temp[i + r][j + c].rgbtBlue;
                        counter++;
                    }
                }
            }

            //  for each pixel calculate the averages collected
            avgR = (int) round(sumR / (float) counter);
            avgG = (int) round(sumG / (float) counter);
            avgB = (int) round(sumB / (float) counter);

            //  for each pixel assign new rgb values to actual image array
            image[i][j].rgbtRed = avgR;
            image[i][j].rgbtBlue = avgB;
            image[i][j].rgbtGreen = avgG;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //  Gx/Gy transformations
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    int GxR;
    int GxG;
    int GxB;
    int GyR;
    int GyG;
    int GyB;
    int R;
    int G;
    int B;

    //  temp array has height and width that is 2 pixels more
    height += 2;
    width += 2;

    //  creating completely black image that has height/ width 2 pixels greater
    RGBTRIPLE temp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i][j].rgbtRed = 0;
            temp[i][j].rgbtGreen = 0;
            temp[i][j].rgbtBlue = 0;
        }
    }

    //  inserting image into temp array with black borders now
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            temp[i][j] = image[i - 1][j - 1];
        }
    }

    //  looping over each row of temp array, targetting only the non-border pixels
    for (int i = 1; i < height - 1; i++)
    { //  looping over each column of temp array, targetting only the non-border pixels
        for (int j = 1; j < width - 1; j++)
        {
            //  reset Gx and Gy values for each pixel's R,G,B
            GxR = 0;
            GxG = 0;
            GxB = 0;
            GyR = 0;
            GyG = 0;
            GyB = 0;
            R = 0;
            G = 0;
            B = 0;

            //  for each pixel, access the surrounding pixels, compute Gx and Gy and add them all up
            for (int r = -1; r <= 1; r++)
            {
                for (int c = -1; c <= 1; c++)
                {
                    GxR += temp[i + r][j + c].rgbtRed * Gx[r + 1][c + 1];
                    GxG += temp[i + r][j + c].rgbtGreen * Gx[r + 1][c + 1];
                    GxB += temp[i + r][j + c].rgbtBlue * Gx[r + 1][c + 1];

                    GyR += temp[i + r][j + c].rgbtRed * Gy[r + 1][c + 1];
                    GyG += temp[i + r][j + c].rgbtGreen * Gy[r + 1][c + 1];
                    GyB += temp[i + r][j + c].rgbtBlue * Gy[r + 1][c + 1];
                }
            }

            //  for each pixel calculate the new R,G,B
            R = (int) round(sqrt(pow((double) GxR, 2) + pow((double) GyR, 2)));
            G = (int) round(sqrt(pow((double) GxG, 2) + pow((double) GyG, 2)));
            B = (int) round(sqrt(pow((double) GxB, 2) + pow((double) GyB, 2)));

            //  ensure RGB are < 255
            if (R > 255)
            {
                R = 255;
            }
            if (G > 255)
            {
                G = 255;
            }
            if (B > 255)
            {
                B = 255;
            }

            //  Assign new RGB values to original image
            image[i - 1][j - 1].rgbtRed = R;
            image[i - 1][j - 1].rgbtGreen = G;
            image[i - 1][j - 1].rgbtBlue = B;
        }
    }

    return;
}
