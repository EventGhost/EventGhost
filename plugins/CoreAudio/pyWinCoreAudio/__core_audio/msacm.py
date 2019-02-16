"""
/* ----------------------------------------------------------------------
 * MP3Player.h C++ class using plain Windows API
 *
 * Author: @lx/Alexandre Mutel,  blog: http://code4k.blogspot.com
 * The software is provided "as is", without warranty of any kind.
 * ----------------------------------------------------------------------*/
#pragma once
#include <windows.h>
#include <stdio.h>
#include <assert.h>
#include <mmreg.h>
#include <msacm.h>
#include <wmsdk.h>

#pragma comment(lib, "msacm32.lib")
#pragma comment(lib, "wmvcore.lib")
#pragma comment(lib, "winmm.lib")
#pragma intrinsic(memset,memcpy,memcmp)

#ifdef _DEBUG
#define mp3Assert(function) assert((function) == 0)
#else
//#define mp3Assert(function) if ( (function) != 0 ) { MessageBoxA(NULL,"Error in [ " #function "]", "Error",MB_OK); ExitProcess(0); }
#define mp3Assert(function) (function)
#endif

/*
 * MP3Player class.
 * Usage :
 *   MP3Player player;
 *   player.OpenFromFile("your.mp3");
 *   player.Play();
 *   Sleep((DWORD)(player.GetDuration()+1));
 *   player.Close();
 */
class MP3Player {
private:
 HWAVEOUT hWaveOut;
 DWORD bufferLength;
 double durationInSecond;
 BYTE* soundBuffer;
public:

 /*
  * OpenFromFile : loads a MP3 file and convert it internaly to a PCM format, ready for sound playback.
  */
 HRESULT OpenFromFile(TCHAR* inputFileName){
  // Open the mp3 file
  HANDLE hFile = CreateFile(inputFileName, // open MYFILE.TXT
         GENERIC_READ,
         FILE_SHARE_READ, // share for reading
         NULL, // no security
         OPEN_EXISTING, // existing file only
         FILE_ATTRIBUTE_NORMAL, // normal file
         NULL); // no attr
  assert( hFile != INVALID_HANDLE_VALUE);

  // Get FileSize
  DWORD fileSize = GetFileSize(hFile, NULL);
  assert( fileSize != INVALID_FILE_SIZE);

  // Alloc buffer for file
  BYTE* mp3Buffer = (BYTE*)LocalAlloc(LPTR, fileSize);

  // Read file and fill mp3Buffer
  DWORD bytesRead;
  DWORD resultReadFile = ReadFile( hFile, mp3Buffer, fileSize, &bytesRead, NULL);
   assert(resultReadFile != 0);
  assert( bytesRead == fileSize);

  // Close File
  CloseHandle(hFile);

  // Open and convert MP3
  HRESULT hr = OpenFromMemory(mp3Buffer, fileSize);

  // Free mp3Buffer
  LocalFree(mp3Buffer);

  return hr;
 }

 /*
  * OpenFromMemory : loads a MP3 from memory and convert it internaly to a PCM format, ready for sound playback.
  */
 HRESULT OpenFromMemory(BYTE* mp3InputBuffer, DWORD mp3InputBufferSize){
  IWMSyncReader* wmSyncReader;
  IWMHeaderInfo* wmHeaderInfo;
  IWMProfile* wmProfile;
  IWMStreamConfig* wmStreamConfig;
  IWMMediaProps* wmMediaProperties;
  WORD wmStreamNum = 0;
  WMT_ATTR_DATATYPE wmAttrDataType;
  DWORD durationInSecondInt;
  QWORD durationInNano;
  DWORD sizeMediaType;
  DWORD maxFormatSize = 0;
  HACMSTREAM acmMp3stream = NULL;
  HGLOBAL mp3HGlobal;
  IStream* mp3Stream;

  // Define output format
  static WAVEFORMATEX pcmFormat = {
   WAVE_FORMAT_PCM, // WORD        wFormatTag;         /* format type */
   2,     // WORD        nChannels;          /* number of channels (i.e. mono, stereo...) */
   44100,    // DWORD       nSamplesPerSec;     /* sample rate */
   4 * 44100,   // DWORD       nAvgBytesPerSec;    /* for buffer estimation */
   4,     // WORD        nBlockAlign;        /* block size of data */
   16,     // WORD        wBitsPerSample;     /* number of bits per sample of mono data */
   0,     // WORD        cbSize;             /* the count in bytes of the size of */
  };

  const DWORD MP3_BLOCK_SIZE = 522;

  // Define input format
  static MPEGLAYER3WAVEFORMAT mp3Format = {
   {

   """

from ctypes.wintypes import DWORD, WORD, HGLOBAL, HRESULT, BYTE
from ctypes import c_ulonglong

MP3_BLOCK_SIZE = DWORD(522)

from mmreg import (
    MPEGLAYER3WAVEFORMAT,
    WAVE_FORMAT_MPEGLAYER3,
    MPEGLAYER3_WFX_EXTRA_BYTES,
    MPEGLAYER3_ID_MPEG,
    MPEGLAYER3_FLAG_PADDING_OFF,
    WAVE_FORMAT_PCM,

)


QWORD = c_ulonglong


"""
    WAVE_FORMAT_MPEGLAYER3,   // WORD        wFormatTag;         /* format type */
     2,        // WORD        nChannels;          /* number of channels (i.e. mono, stereo...) */
     44100,       // DWORD       nSamplesPerSec;     /* sample rate */
     128 * (1024 / 8),    // DWORD       nAvgBytesPerSec;    not really used but must be one of 64, 96, 112, 128, 160kbps
     1,        // WORD        nBlockAlign;        /* block size of data */
     0,        // WORD        wBitsPerSample;     /* number of bits per sample of mono data */
     MPEGLAYER3_WFX_EXTRA_BYTES,  // WORD        cbSize;
   },
   MPEGLAYER3_ID_MPEG,      // WORD          wID;
   MPEGLAYER3_FLAG_PADDING_OFF,   // DWORD         fdwFlags;
   MP3_BLOCK_SIZE,       // WORD          nBlockSize;
   1,          // WORD          nFramesPerBlock;
   1393,         // WORD          nCodecDelay;
  };

  // -----------------------------------------------------------------------------------
  // Extract and verify mp3 info : duration, type = mp3, sampleRate = 44100, channels = 2
  // -----------------------------------------------------------------------------------

  // Initialize COM
  CoInitialize(0);

  // Create SyncReader
  mp3Assert( WMCreateSyncReader(  NULL, WMT_RIGHT_PLAYBACK , &wmSyncReader ) );

  // Alloc With global and create IStream
  mp3HGlobal = GlobalAlloc(GPTR, mp3InputBufferSize);
  assert(mp3HGlobal != 0);
  void* mp3HGlobalBuffer = GlobalLock(mp3HGlobal);
  memcpy(mp3HGlobalBuffer, mp3InputBuffer, mp3InputBufferSize);
  GlobalUnlock(mp3HGlobal);
  mp3Assert( CreateStreamOnHGlobal(mp3HGlobal, FALSE, &mp3Stream) );

  // Open MP3 Stream
  mp3Assert( wmSyncReader->OpenStream(mp3Stream) );

  // Get HeaderInfo interface
  mp3Assert( wmSyncReader->QueryInterface(&wmHeaderInfo) );

  // Retrieve mp3 song duration in seconds
  WORD lengthDataType = sizeof(QWORD);
  mp3Assert( wmHeaderInfo->GetAttributeByName(&wmStreamNum, L"Duration", &wmAttrDataType, (BYTE*)&durationInNano, &lengthDataType ) );
  durationInSecond = ((double)durationInNano)/10000000.0;
  durationInSecondInt = (int)(durationInNano/10000000)+1;

  // Sequence of call to get the MediaType
  // WAVEFORMATEX for mp3 can then be extract from MediaType
  mp3Assert( wmSyncReader->QueryInterface(&wmProfile) );
  mp3Assert( wmProfile->GetStream(0, &wmStreamConfig) );
  mp3Assert( wmStreamConfig->QueryInterface(&wmMediaProperties) );

  // Retrieve sizeof MediaType
  mp3Assert( wmMediaProperties->GetMediaType(NULL, &sizeMediaType) );

  // Retrieve MediaType
  WM_MEDIA_TYPE* mediaType = (WM_MEDIA_TYPE*)LocalAlloc(LPTR,sizeMediaType);
  mp3Assert( wmMediaProperties->GetMediaType(mediaType, &sizeMediaType) );

  // Check that MediaType is audio
  assert(mediaType->majortype == WMMEDIATYPE_Audio);
  // assert(mediaType->pbFormat == WMFORMAT_WaveFormatEx);

  // Check that input is mp3
  WAVEFORMATEX* inputFormat = (WAVEFORMATEX*)mediaType->pbFormat;
  assert( inputFormat->wFormatTag == WAVE_FORMAT_MPEGLAYER3);
  assert( inputFormat->nSamplesPerSec == 44100);
  assert( inputFormat->nChannels == 2);

  // Release COM interface
  // wmSyncReader->Close();
  wmMediaProperties->Release();
  wmStreamConfig->Release();
  wmProfile->Release();
  wmHeaderInfo->Release();
  wmSyncReader->Release();

  // Free allocated mem
  LocalFree(mediaType);

  // -----------------------------------------------------------------------------------
  // Convert mp3 to pcm using acm driver
  // The following code is mainly inspired from http://david.weekly.org/code/mp3acm.html
  // -----------------------------------------------------------------------------------

  // Get maximum FormatSize for all acm
  mp3Assert( acmMetrics( NULL, ACM_METRIC_MAX_SIZE_FORMAT, &maxFormatSize ) );

  // Allocate PCM output sound buffer
  bufferLength = durationInSecond * pcmFormat.nAvgBytesPerSec;
  soundBuffer = (BYTE*)LocalAlloc(LPTR, bufferLength);

  acmMp3stream = NULL;
  switch ( acmStreamOpen( &acmMp3stream,    // Open an ACM conversion stream
   NULL,                       // Query all ACM drivers
   (LPWAVEFORMATEX)&mp3Format, // input format :  mp3
   &pcmFormat,                 // output format : pcm
   NULL,                       // No filters
   0,                          // No async callback
   0,                          // No data for callback
   0                           // No flags
   )
   ) {
      case MMSYSERR_NOERROR:
       break; // success!
      case MMSYSERR_INVALPARAM:
       assert( !"Invalid parameters passed to acmStreamOpen" );
       return E_FAIL;
      case ACMERR_NOTPOSSIBLE:
       assert( !"No ACM filter found capable of decoding MP3" );
       return E_FAIL;
      default:
       assert( !"Some error opening ACM decoding stream!" );
       return E_FAIL;
  }

  // Determine output decompressed buffer size
  unsigned long rawbufsize = 0;
  mp3Assert( acmStreamSize( acmMp3stream, MP3_BLOCK_SIZE, &rawbufsize, ACM_STREAMSIZEF_SOURCE ) );
  assert( rawbufsize > 0 );

  // allocate our I/O buffers
  static BYTE mp3BlockBuffer[MP3_BLOCK_SIZE];
  //LPBYTE mp3BlockBuffer = (LPBYTE) LocalAlloc( LPTR, MP3_BLOCK_SIZE );
  LPBYTE rawbuf = (LPBYTE) LocalAlloc( LPTR, rawbufsize );

  // prepare the decoder
  static ACMSTREAMHEADER mp3streamHead;
  // memset( &mp3streamHead, 0, sizeof(ACMSTREAMHEADER ) );
  mp3streamHead.cbStruct = sizeof(ACMSTREAMHEADER );
  mp3streamHead.pbSrc = mp3BlockBuffer;
  mp3streamHead.cbSrcLength = MP3_BLOCK_SIZE;
  mp3streamHead.pbDst = rawbuf;
  mp3streamHead.cbDstLength = rawbufsize;
  mp3Assert( acmStreamPrepareHeader( acmMp3stream, &mp3streamHead, 0 ) );

  BYTE* currentOutput = soundBuffer;
  DWORD totalDecompressedSize = 0;

  static ULARGE_INTEGER newPosition;
  static LARGE_INTEGER seekValue;
  mp3Assert( mp3Stream->Seek(seekValue, STREAM_SEEK_SET, &newPosition) );

  while(1) {
   // suck in some MP3 data
   ULONG count;
   mp3Assert( mp3Stream->Read(mp3BlockBuffer, MP3_BLOCK_SIZE, &count) );
   if( count != MP3_BLOCK_SIZE )
    break;

   // convert the data
   mp3Assert( acmStreamConvert( acmMp3stream, &mp3streamHead, ACM_STREAMCONVERTF_BLOCKALIGN ) );

   // write the decoded PCM to disk
   //count = fwrite( rawbuf, 1, mp3streamHead.cbDstLengthUsed, fpOut );
   memcpy(currentOutput, rawbuf, mp3streamHead.cbDstLengthUsed);
   totalDecompressedSize += mp3streamHead.cbDstLengthUsed;
   currentOutput += mp3streamHead.cbDstLengthUsed;
  };

  mp3Assert( acmStreamUnprepareHeader( acmMp3stream, &mp3streamHead, 0 ) );
  LocalFree(rawbuf);
  mp3Assert( acmStreamClose( acmMp3stream, 0 ) );

  // Release allocated memory
  mp3Stream->Release();
  GlobalFree(mp3HGlobal);
  return S_OK;
 }

 /*
  * Close : close the current MP3Player, stop playback and free allocated memory
  */
 void __inline Close() {
  // Reset before close (otherwise, waveOutClose will not work on playing buffer)
  waveOutReset(hWaveOut);
  // Close the waveOut
  waveOutClose(hWaveOut);
  // Free allocated memory
  LocalFree(soundBuffer);
 }

 /*
  * GetDuration : return the music duration in seconds
  */
 double __inline GetDuration() {
  return durationInSecond;
 }

 /*
  * GetPosition : return the current position from the sound playback (used from sync)
  */
 double GetPosition() {
  static MMTIME MMTime = { TIME_SAMPLES, 0};
  waveOutGetPosition(hWaveOut, &MMTime, sizeof(MMTIME));
  return ((double)MMTime.u.sample)/( 44100.0);
 }

 /*
  * Play : play the previously opened mp3
  */
 void Play() {
  static WAVEHDR WaveHDR = { (LPSTR)soundBuffer,  bufferLength };

  // Define output format
  static WAVEFORMATEX pcmFormat = {
   WAVE_FORMAT_PCM, // WORD        wFormatTag;         /* format type */
   2,     // WORD        nChannels;          /* number of channels (i.e. mono, stereo...) */
   44100,    // DWORD       nSamplesPerSec;     /* sample rate */
   4 * 44100,   // DWORD       nAvgBytesPerSec;    /* for buffer estimation */
   4,     // WORD        nBlockAlign;        /* block size of data */
   16,     // WORD        wBitsPerSample;     /* number of bits per sample of mono data */
   0,     // WORD        cbSize;             /* the count in bytes of the size of */
  };

  mp3Assert( waveOutOpen( &hWaveOut, WAVE_MAPPER, &pcmFormat, NULL, 0, CALLBACK_NULL ) );
  mp3Assert( waveOutPrepareHeader( hWaveOut, &WaveHDR, sizeof(WaveHDR) ) );
  mp3Assert( waveOutWrite  ( hWaveOut, &WaveHDR, sizeof(WaveHDR) ) );
 }
};

#pragma function(memset,memcpy,memcmp)
"""

from mmreg import WAVEFORMATEX, MPEGLAYER3WAVEFORMAT
