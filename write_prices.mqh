//+------------------------------------------------------------------+
//|                                                  python_comm.mqh |
//|                                                  Oguz Alp Saglam |
//|                https://www.linkedin.com/in/oguzalp-saglam961881/ |
//+------------------------------------------------------------------+
#property copyright "Oguz Alp Saglam"
#property link      "https://www.linkedin.com/in/oguzalp-saglam961881/"
#property strict
//+------------------------------------------------------------------+
//| defines                                                          |
//+------------------------------------------------------------------+
// #define MacrosHello   "Hello, world!"
// #define MacrosYear    2010
//+------------------------------------------------------------------+
//| DLL imports                                                      |
//+------------------------------------------------------------------+
// #import "user32.dll"
//   int      SendMessageA(int hWnd,int Msg,int wParam,int lParam);
// #import "my_expert.dll"
//   int      ExpertRecalculate(int wParam,int lParam);
// #import
//+------------------------------------------------------------------+
//| EX5 imports                                                      |
//+------------------------------------------------------------------+
// #import "stdlib.ex5"
//   string ErrorDescription(int error_code);
// #import
//+------------------------------------------------------------------+
//#include <Mql/Utils/File>

/*void create_folder(string folder_name){
   File::createFolder(folder_name);
}

void write_prices(string pair){
   try{
      create_folder("datasets");
   }catch(int e){
      Alert("Folder already exists...");
   }
   CsvFile csv("datasets\\"+ pair +".csv",FILE_WRITE);
   
}*/

void write_prices(){
   int file_handle = FileOpen(_Symbol+ _Period + ".csv", FILE_WRITE|FILE_CSV);
   FileWriteString(file_handle, "Open,Close,High,Low,Time,Volume\n");
   for(int i=Bars - 1;i>0;i--){
     string s = Open[i] + "," + Close[i] + "," + High[i] + "," + Low[i] + "," + Time[i] + "," + Volume[i] + "\n";
     FileWriteString(file_handle, s);
   }
}
