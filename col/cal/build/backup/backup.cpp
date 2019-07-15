/*
 * class Cal:
 * Function:
 * 1. filterMake
 * 2. filterRun
 * 3. rawData2Data
 * 4. changeStat
 */

typedef unsigned char uchr;
#define filterMaxNum  	15
#define channelMaxNum	256
#define filterMaxOrder	330

class Cal{
	public:
		void makeFilter(double* a, double* b, int order, int index);
		int run(uchr* data, double*resData, int length);
		void changeStat(int stat, int index);
		// --- {{{ PROTECTED SECTION
		double filterA[filterMaxNum][filterMaxOrder] = {0};
		double filterB[filterMaxNum][filterMaxOrder] = {0};
		double filterSrc[filterMaxNum*channelMaxNum][filterMaxOrder] = {0};
		double filterFit[filterMaxNum*channelMaxNum][filterMaxOrder] = {0};
		double resDataSingleTemp[channelMaxNum] = {0};
		int filterRecord[filterMaxNum] = {0};
		int filterIndexList[filterMaxOrder] = {0};
		int channelNum;
		int bagEachLen;
		int rawData2Data(uchr* rawData, double* resData, int length);
		void runFilter(double* data, double* resData);
		// --- }}}
		// --- {{{ PRIVATE SECTION
		int judgeBagHead(uchr* data);
		int judgeRawData(uchr* data);
		void clearFilterData(void);
		void singleFilter(double* rawdata);
		void singleFilterRecord(double* rawData);
		void filterIndexListInit();
		void filterIndexListRefresh();
		// --- }}}
};

// --- {{{ Change status
void Cal::changeStat(int statData, int index){
	/*
	 * Index 
	 * 0 : channelNum
	 */
	// --- {{{ Code
	clearFilterData();
	filterIndexListInit();
	if(index == 0){
		channelNum = statData;
		bagEachLen = 2*channelNum + 1 + 5;
	}
	// --- }}}

}
// ---}}}
// --- {{{ RawDataChar to DataDouble
int Cal::rawData2Data(uchr* rawData, double* resData, int length){
	/*
	 * numRigth : Correct Data Num
	 */
	// --- {{{ Code
	int judge = 0;
	int index = 0;
	int numRight = 0;
	uchr* pData;
	for(int i=0; i<length / bagEachLen; i++){
		pData = rawData + bagEachLen*i;
		judge = judgeRawData(pData);
		if(judge == 0){
			numRight++;
			pData = pData + 5;
			for(int j=0; j < channelNum*2; j++){
				if(j % 2 == 0){
					resData[index] = (pData[j] << 8);
				}
				else{
					resData[index] += pData[j];
					index++;
				}
			}
		}
	}
	return numRight;
	// ---}}}
}
// --- }}}
// --- {{{ Make Appointed FilterList a & b
void Cal::makeFilter(double* a, double* b, int order, int index){
	/*
	 * 
	 */
	// --- {{{  Code
	for(int i=0; i<order; i++){
		filterA[index][i] = a[i];
		filterB[index][i] = b[i];
	}
	filterRecord[index] = order;
	// --- }}}

}
// --- }}}
// --- {{{ Filter singlerawData through all filter
void Cal::runFilter(double* data, double* resData){
	/*
	 *
	 */
	// --- {{{ Code
	int tempIndex;
	double tempRes;
	int k;
	for(int i=0; i<channelNum; i++){
		tempRes = data[i];
		for(int j=0; j<filterMaxNum; j++){
			if(filterRecord[j] != 0){
				tempIndex = filterRecord[j];
				filterSrc[j*channelNum+i][filterIndexList[0]] = tempRes;
				tempRes = tempRes*filterB[j][0];
				if(j != 0){
					for(int k=1; k<tempIndex; k++){
						tempRes += (filterSrc[j*channelNum+i][filterIndexList[k]]*filterB[j][k]
								- filterFit[j*channelNum+i][filterIndexList[k]]*filterA[j][k]);
					}
				}
				else{
					tempRes += (filterSrc[j*channelNum+i][filterIndexList[tempIndex-1]]*filterB[j][tempIndex-1]
							- filterFit[j*channelNum+i][filterIndexList[tempIndex-1]]*filterA[j][tempIndex-1]);
				}
				filterFit[j*channelNum+i][filterIndexList[0]] = tempRes;
			}
		}
		resData[i] = tempRes;
	}
	filterIndexListRefresh();
	// --- }}}

}
// --- }}}
// --- {{{ Judge Bag Head
int Cal::judgeBagHead(uchr* data){
	/*
	 * Return Num:
	 * 0 : All Right
	 * -1: BagHeadHeadLost
	 * -2: BagHeadCheckWrong
	 * -3: WrongUploadData
	 * -4: HardWareStatWrong
	 * -5: ChannelNumWrong
	 */
	// --- {{{ Code
	int chanTCP;
	uchr judge;
	if(!((data[0] == 0x55) & (data[1] == 0xAA))){
		return -1;
	}
	judge = data[2] + data[3];
	if(!(judge == data[4])){
		return -2;
	}
	if (!(data[2] & 0x10)){
		return -3;
	}
	if (!(data[2] & 0x08)){
		return -4;
	}
	chanTCP = data[3] + 1;
	if (chanTCP != channelNum){
		return -5;
	}
	return 0;
	// --- }}}
}
// --- }}}
// --- {{{ Judge Data
int Cal::judgeRawData(uchr* data){
	/*
	 * 1: DataSentWrong
	 */
	int judgeHead = 0;
	uchr judgeData = 0;
	uchr* pData;
	judgeHead = judgeBagHead(data);
	if (judgeHead == 0){
		pData = data + 5;
		for(int i=0; i < 2*channelNum; i++){
			judgeData += pData[i];
		}
		if (judgeData == data[bagEachLen-1]){
			return 0;
		}
		else{
			return 1;
		}
	}
	else{
		return judgeHead;
	}

}
// --- }}}
// --- {{{ Clear Filter Data
void Cal::clearFilterData(void){
	int filterNum;
	for(int i=0; i < filterMaxNum; i++){
		if(filterRecord[i] != 0){
			filterNum++;
		}
	}
	for(int i=0; i<filterNum*channelNum; i++){
		for(int j=0; j<filterMaxOrder; j++){
			filterSrc[i][j] = 0;
			filterFit[i][j] = 0;
		}
	}
}
// --- }}}
// --- {{{ FilterIndexList Initial
void Cal::filterIndexListInit(void){
	/*
	 *
	 */
	// --- {{{ Code 
	// filter
	for(int i=0; i<filterMaxOrder; i++){
		filterIndexList[i] = i;
	}
	// --- }}}
}
// --- }}}
// --- {{{ FilterIndexList Refresh
void Cal::filterIndexListRefresh(void){
	/*
	 *
	 */
	// --- {{{ Code 
	int temp = filterIndexList[filterMaxOrder-1];
	for(int i=filterMaxOrder-1; i>0; i--){
		filterIndexList[i] = filterIndexList[i-1];
	}
	filterIndexList[0] = temp;
	// --- }}}


}
// --- }}}
// --- {{{ Run 
int Cal::run(uchr* data, double* resData, int length){
	/*
	 */
	// --- {{{ Code 
	int num = rawData2Data(data, resData, length);
	for(int i=0; i<num; i++){
		runFilter(resData+i*channelNum, resData+i*channelNum);
	}
	return num;
	// --- }}}
}
// --- }}}

extern "C"{
	Cal cal;
	void makeFilter(double* a, double* b, int order, int index){
		cal.makeFilter(a, b, order, index);
	};
	void changeStat(int statData, int index){
		cal.changeStat(statData, index);
	}
	int run(uchr* data, double* resData, int length){
		int res = cal.run(data, resData, length);
		return res;
	}
}
