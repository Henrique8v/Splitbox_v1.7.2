#include <windows.h>
#include <mmdeviceapi.h>
#include <endpointvolume.h>
#include <audiopolicy.h>
#include <psapi.h>

// Exportação para o Python
extern "C" __declspec(dllexport) bool SetMute(HWND targetHwnd, bool mute) {
    DWORD targetPid;
    GetWindowThreadProcessId(targetHwnd, &targetPid);

    HRESULT hr = CoInitialize(NULL);
    if (FAILED(hr)) return false;

    IMMDeviceEnumerator* enumerator = NULL;
    hr = CoCreateInstance(__uuidof(MMDeviceEnumerator), NULL, CLSCTX_ALL, __uuidof(IMMDeviceEnumerator), (void**)&enumerator);
    
    if (SUCCEEDED(hr)) {
        IMMDevice* device = NULL;
        hr = enumerator->GetDefaultAudioEndpoint(eRender, eMultimedia, &device);
        
        if (SUCCEEDED(hr)) {
            IAudioSessionManager2* manager = NULL;
            hr = device->Activate(__uuidof(IAudioSessionManager2), CLSCTX_ALL, NULL, (void**)&manager);
            
            if (SUCCEEDED(hr)) {
                IAudioSessionEnumerator* sessionEnumerator = NULL;
                hr = manager->GetSessionEnumerator(&sessionEnumerator);
                
                if (SUCCEEDED(hr)) {
                    int sessionCount = 0;
                    sessionEnumerator->GetCount(&sessionCount);
                    
                    for (int i = 0; i < sessionCount; i++) {
                        IAudioSessionControl* control = NULL;
                        hr = sessionEnumerator->GetSession(i, &control);
                        
                        if (SUCCEEDED(hr)) {
                            IAudioSessionControl2* control2 = NULL;
                            hr = control->QueryInterface(__uuidof(IAudioSessionControl2), (void**)&control2);
                            
                            if (SUCCEEDED(hr)) {
                                DWORD sessionPid = 0;
                                control2->GetProcessId(&sessionPid);
                                
                                if (sessionPid == targetPid) {
                                    ISimpleAudioVolume* volume = NULL;
                                    hr = control2->QueryInterface(__uuidof(ISimpleAudioVolume), (void**)&volume);
                                    if (SUCCEEDED(hr)) {
                                        volume->SetMute(mute, NULL);
                                        volume->Release();
                                    }
                                }
                                control2->Release();
                            }
                            control->Release();
                        }
                    }
                    sessionEnumerator->Release();
                }
                manager->Release();
            }
            device->Release();
        }
        enumerator->Release();
    }
    CoUninitialize();
    return true;
}