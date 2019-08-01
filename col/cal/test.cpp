/*
 * class Test
 * Function:
 * 1 . featExact
 */

#include <iostream>
#include <cmath>
#define DOUBLE_PI 6.283185307179586476925286766559
using namespace std;


class Test{
	public:
		// -- {{{ PUBLIC SECTION
		void featExact(double* data);
		void test(double* data, int len);
		// }}}
	protected:
		// --- {{{ PROTECTED SECTION
		// Time Domain Features
		double variance(double* data, int len);
		int zeroCrossings(double* data, int len);
		double logDetector(double* data, int len);
		int slopeSignChange(double* data, int len);
		int willisonAmplitude(double* data, int len);
		double waveformLength(double *data, int len);
		double meanAbsoluteValue(double* data, int len);
		// Frequency Domain Features
		void FFT(double* xreal, double* ximag, int len);
		void IFFT(double* xreal, double* ximag, int len);
		// }}}
	private:
		inline void swap(double &a, double &b);
		void bitrp(double* xreal, double* ximag, int len);
		// --- {{{ PRIVATE SECTION
		// }}}
};

// --- {{{ featExact
void Test::featExact(double* data){
}
// --- }}}
// --- {{{ MeanAbsoluteValue
double Test::meanAbsoluteValue(double* data, int len){
	double res = 0;
	for(int i=0; i<len; i++){
		res += fabs(data[i]);
	}
	if(len == 0) return 0;
	else return res / len;
}
// ---}}}
//  --- {{{ Variance
double Test::variance(double* data, int len){
	double res;
	for(int i=0; i<len; i++){
		res += data[i]*data[i];
	}
	if(len <= 1) return 0;
	else return res / (len - 1);
}
//  }}}
// --- {{{ ZeroCrossings
int Test::zeroCrossings(double* data, int len){
	double epsilon = 0.001;
	int res = 0;
	for(int i=0; i<len-1; i++){
		if((data[i]*data[i+1] < 0) 
				& (fabs(data[i] - data[i+1]) >= epsilon)){
			res += 1;
		}
	}
	if(len <= 1) return 0;
	else return res;
}
// }}}
// --- {{{ slopeSignChange
int Test::slopeSignChange(double* data, int len){
	double epsilon = 0.001;
	int res = 0;
	for (int i=0; i<len-2; i++){
		if((((data[i] < data[i+1]) & (data[i+1] < data[i+2])) 
					| ((data[i] > data[i+1]) | (data[i+1] > data[i+2]))) 
				& ((fabs(data[i] - data[i+1]) >= epsilon) 
					| (fabs(data[i+1] - data[i+2]) >= epsilon))){
			res += 1;
		}
	}
	if (len <= 2) return 0;
	else return res;
}
// }}}
// --- {{{ waveFormLength
double Test::waveformLength(double* data, int len){
	double res = 0;
	for(int i=0; i<len-1; i++){
		res += fabs(data[i] - data[i+1]);
	}
	if(len <= 1) return 0;
	else return res;
}
// }}}
// --- {{{ willisonAmplitude
int Test::willisonAmplitude(double* data, int len){
	double epsilon = 0.001;
	int res = 0;
	for(int i=0; i<len-1; i++){
		if(fabs(data[i] - data[i+1]) > epsilon){
			res += 1;
		}
	}
	if(len <= 1) return 0;
	else return res;
}
// }}}
// --- {{{ logDetector
double Test::logDetector(double* data, int len){
	double res = 0;
	for(int i=0; i<len; i++){
		if(data[i] != 0){
			res += log(fabs(data[i]));
		}
	}
	if(len == 0) return 0;
	else return exp(res / len);
}
// }}}
// --- {{{ swap
inline void Test::swap(double &a, double &b){
	double t;
	t = a;
	a = b;
	b = t;
}
// }}}
// --- {{{ bitrp
void bitrp(double* xreal, double* ximag, int len){
	int i, j, a, b, p;
	for(i=1, p=0; i<n; i*=2) p++;
	for(i=0; i<n; i++){
		a = i;
		b = 0;
		for(j=0; j<p; j++){
			b = (b << 1) + (a & 1);
			a >>= 1;
		}
		if(b > i){
			swap(xreal[i], xreal[b]);
			swap(ximag[i], ximag[b]);
		}
	}
}
// }}}
// ---{{{ FFT
// }}}
// --- {{{ test
void Test::test(double* data, int len){
	double res = logDetector(data, len);
	cout << res;
}
// ---}}}

extern "C"{
	Test cal;
	void featExact(double* data){
		cal.featExact(data);
	}
	void test(double* data, int len){
		cal.test(data, len);
	}
}
