import os, sys, glob, shutil, subprocess, json, locale
import urllib.request
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

if os.name == 'nt':
    os.system('chcp 65001')
    os.system('')

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PARENT_DIR = os.path.dirname(BASE_DIR)

DRIVE_IN = os.path.join(PARENT_DIR, 'input')
DRIVE_OUT = os.path.join(PARENT_DIR, 'output')
TEMP_IN = os.path.join(BASE_DIR, 'temp_in')
TEMP_OUT = os.path.join(BASE_DIR, 'temp_out')
SETTINGS_DIR = os.path.join(PARENT_DIR, 'settings')
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'settings.json')

try:
    sys_lang = locale.getdefaultlocale()[0]
    USER_LANG = 'ko' if sys_lang and sys_lang.startswith('ko') else 'en'
except:
    USER_LANG = 'en'

I18N = {
    'ko': {
        'pause_msg': "\n엔터 키를 누르면 프로그램이 종료됩니다...",
        'err_ffmpeg': "FFmpeg를 찾을 수 없습니다.\n프로그램 폴더 안에 'ffmpeg.exe'를 함께 넣어주세요.",
        'install_py': "시스템에 호환 버전(Python 3.10)이 없어 자동 설치를 시작합니다...",
        'install_py_done': "파이썬 설치가 완료되었습니다. 프로그램을 종료 후 다시 실행해 주세요.",
        'err_py_install': "자동 설치 오류: {}",
        'err_no_py': "파이썬 3.10을 찾을 수 없습니다.",
        'install_module': "AI 분리 모듈을 설치합니다. (5~20분 소요)\n",
        'err_module_install': "자동 설치 중 문제가 발생했습니다.",
        'err_no_exe': "실행 파일을 찾을 수 없습니다. PC를 재부팅해 보세요.",
        'load_prev': "[이전 설정 불러오기]",
        'prev_model': " - 사용 모델: {}",
        'prev_stems': " - 추출 대상: {}",
        'prompt_prev': "이 설정 그대로 진행하려면 [Enter]를 누르세요. (새로 설정하려면 'n' 입력): ",
        'menu_title': " 🎧 [음원 분리 모드 선택]",
        'menu_1': " 1. 보컬 전용 (Vocal) - 보컬 추출에 특화",
        'menu_2': " 2. 반주 전용 (Inst)  - MR 추출에 특화",
        'menu_3': " 3. 4트랙 악기 분리   - 보컬, 드럼, 베이스, 기타(Other)로 분리",
        'prompt_mode': "원하시는 모드의 번호를 입력하세요 (1/2/3): ",
        'err_mode': "잘못된 입력입니다. 1, 2, 3 중에서 다시 선택해주세요.",
        'menu_4track': "\n [4트랙 분리 - 추출 대상 다중 선택]",
        'menu_4track_items': " 1: 보컬(vocals), 2: 드럼(drums), 3: 베이스(bass), 4: 기타/건반(other)",
        'prompt_4track': " 추출할 번호를 띄어쓰기나 쉼표로 구분해 입력하세요: ",
        'err_4track': " 잘못된 입력입니다. 1~4 사이의 숫자를 입력해 주세요.",
        'err_no_files': "'{}' 폴더에 작업할 오디오 파일이 없습니다.",
        'start_work': "\n총 {}개 파일 작업 시작 (선택된 모델: {})\n",
        'err_storage': "중단: 저장 공간 부족!",
        'skip_file': " ➔ 이미 완료된 파일 (스킵)",
        'pre_process': " ➔ 오디오 분할 전처리 중...",
        'separating': " ➔ 분리 작업 중 [{}] {:5.1f}% ({}/{})",
        'merging': " ➔ 트랙별 MP3 병합 중...",
        'done': " ➔ 분리 완료!",
        'all_done': "\n모든 작업이 종료되었습니다. 'output' 폴더를 확인하세요.",
        'model_voc': "보컬 전용 (Vocals)",
        'model_inst': "반주 전용 (Instrumental)",
        'model_4tr': "4트랙 악기 분리"
    },
    'en': {
        'pause_msg': "\nPress Enter to exit the program...",
        'err_ffmpeg': "FFmpeg not found.\nPlease place 'ffmpeg.exe' in the program folder.",
        'install_py': "Compatible Python 3.10 not found. Starting automatic installation...",
        'install_py_done': "Python installation complete. Please restart the program.",
        'err_py_install': "Auto-installation error: {}",
        'err_no_py': "Python 3.10 not found.",
        'install_module': "Installing AI separation module. (Takes 5-20 minutes)\n",
        'err_module_install': "An error occurred during automatic installation.",
        'err_no_exe': "Executable file not found. Try rebooting your PC.",
        'load_prev': "[Load Previous Settings]",
        'prev_model': " - Model used: {}",
        'prev_stems': " - Target stems: {}",
        'prompt_prev': "Press [Enter] to proceed with these settings. (Enter 'n' to setup anew): ",
        'menu_title': "[Audio Separation Mode Selection]",
        'menu_1': " 1. Vocals Only - Specialized in vocal extraction",
        'menu_2': " 2. Instrumental Only - High-quality MR extraction",
        'menu_3': " 3. 4-Track Stems - Separate into Vocals, Drums, Bass, and Other",
        'prompt_mode': "Enter the number of your desired mode (1/2/3): ",
        'err_mode': "Invalid input. Please choose from 1, 2, or 3.",
        'menu_4track': "\n [4-Track Separation - Multiple Stem Selection]",
        'menu_4track_items': " 1: Vocals, 2: Drums, 3: Bass, 4: Other",
        'prompt_4track': "Enter the numbers to extract, separated by space or comma: ",
        'err_4track': " Invalid input. Please enter a number between 1 and 4.",
        'err_no_files': "No audio files found in the '{}' folder.",
        'start_work': "\nStarting processing for {} files (Selected model: {})\n",
        'err_storage': "Aborted: Insufficient storage space!",
        'skip_file': " ➔ Already processed (Skipped)",
        'pre_process': " ➔ Pre-processing audio chunking...",
        'separating': " ➔ Separating [{}] {:5.1f}% ({}/{})",
        'merging': " ➔ Merging MP3 tracks...",
        'done': " ➔ Separation complete!",
        'all_done': "\nAll tasks completed. Please check the 'output' folder.",
        'model_voc': "Vocals Only",
        'model_inst': "Instrumental Only",
        'model_4tr': "4-Track Stems"
    }
}

def _t(key, *args):
    text = I18N.get(USER_LANG, I18N['en']).get(key, key)
    return text.format(*args) if args else text

def pause_and_exit(msg):
    print(msg)
    input(_t('pause_msg'))
    sys.exit()

def prt(m, nl=False):
    sys.stdout.write(f"\r{m: <100}")
    sys.stdout.flush()
    if nl: sys.stdout.write("\n")

def get_ffmpeg_path():
    local_ffmpeg = os.path.join(BASE_DIR, 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg): return local_ffmpeg
    system_ffmpeg = shutil.which('ffmpeg')
    if system_ffmpeg: return system_ffmpeg
    pause_and_exit(_t('err_ffmpeg'))

def get_python310_cmd():
    try:
        subprocess.run(["py", "-3.10", "--version"], capture_output=True, check=True)
        return ["py", "-3.10"]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    py_path = shutil.which('python')
    if py_path:
        try:
            out = subprocess.check_output([py_path, "--version"], text=True)
            if "3.10" in out: return [py_path]
        except Exception:
            pass
    return None

def install_python_if_needed():
    if get_python310_cmd() is not None: return True
    print(_t('install_py'))
    
    installer_url = "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
    installer_path = os.path.join(BASE_DIR, "python_installer.exe")
    try:
        urllib.request.urlretrieve(installer_url, installer_path)
        subprocess.run([installer_path, "/passive", "InstallAllUsers=1", "PrependPath=1"], check=True)
        if os.path.exists(installer_path): os.remove(installer_path)
        pause_and_exit(_t('install_py_done'))
    except Exception as e:
        pause_and_exit(_t('err_py_install', e))

def check_and_install_dependencies():
    py_cmd = get_python310_cmd()
    if not py_cmd: pause_and_exit(_t('err_no_py'))
    try:
        subprocess.run(py_cmd + ["-c", "import audio_separator"], capture_output=True, check=True)
        return py_cmd
    except subprocess.CalledProcessError:
        pass
    
    print(_t('install_module'))
    try:
        subprocess.run(py_cmd + ["-m", "pip", "install", "--upgrade", "pip"], check=True)
        subprocess.run(py_cmd + ["-m", "pip", "install", "audio-separator[gpu]"], check=True)
        return py_cmd
    except subprocess.CalledProcessError:
        pause_and_exit(_t('err_module_install'))

def get_audio_separator_path(py_cmd):
    try:
        script_code = "import os, sys; print(os.path.join(os.path.dirname(sys.executable), 'Scripts', 'audio-separator.exe'))"
        exe_path = subprocess.check_output(py_cmd + ["-c", script_code], text=True).strip()
        if os.path.exists(exe_path): return exe_path
        
        script_code_user = "import os, site; print(os.path.join(site.getuserbase(), 'Scripts', 'audio-separator.exe'))"
        exe_path_user = subprocess.check_output(py_cmd + ["-c", script_code_user], text=True).strip()
        if os.path.exists(exe_path_user): return exe_path_user
    except Exception:
        pass
    return shutil.which('audio-separator')

def select_mode():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
            prev_model = saved.get('model_name')
            prev_stems = saved.get('target_stems')
            
            model_disp_name = {
                'UVR-MDX-NET-Voc_FT.onnx': _t('model_voc'),
                'UVR-MDX-NET-Inst_HQ_3.onnx': _t('model_inst'),
                'htdemucs_ft.yaml': _t('model_4tr')
            }.get(prev_model, prev_model)
            
            print("\n====================================================================")
            print(_t('load_prev'))
            print(_t('prev_model', model_disp_name))
            print(_t('prev_stems', ', '.join(prev_stems)))
            print("====================================================================")
            ans = input(_t('prompt_prev')).strip().lower()
            
            if ans == '':
                return prev_model, prev_stems
        except Exception:
            pass 
    
    print("\n====================================================================")
    print(_t('menu_title'))
    print(_t('menu_1'))
    print(_t('menu_2'))
    print(_t('menu_3'))
    print("====================================================================")
    
    while True:
        mode = input(_t('prompt_mode')).strip()
        
        if not mode:
            sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
            continue
            
        if mode == '1':
            model, stems = 'UVR-MDX-NET-Voc_FT.onnx', ['Vocals']
            break
        elif mode == '2':
            model, stems = 'UVR-MDX-NET-Inst_HQ_3.onnx', ['Instrumental']
            break
        elif mode == '3':
            model = 'htdemucs_ft.yaml'
            print(_t('menu_4track'))
            print(_t('menu_4track_items'))
            
            while True:
                sub_choice = input(_t('prompt_4track')).strip()
                
                if not sub_choice:
                    sys.stdout.write("\033[F\033[K")
                    sys.stdout.flush()
                    continue
                
                stem_map = {'1': 'vocals', '2': 'drums', '3': 'bass', '4': 'other'}
                parts = sub_choice.replace(',', ' ').split()
                stems = []
                for p in parts:
                    if p in stem_map and stem_map[p] not in stems:
                        stems.append(stem_map[p])
                
                if stems:
                    break
                else:
                    print(_t('err_4track'))
            break
        
        print(_t('err_mode'))
    
    try:
        os.makedirs(SETTINGS_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({'model_name': model, 'target_stems': stems}, f, ensure_ascii=False, indent=4)
    except Exception:
        pass
    
    return model, stems

def main():
    install_python_if_needed()
    ffmpeg_exe = get_ffmpeg_path()
    py_cmd = check_and_install_dependencies()
    
    audio_separator_exe = get_audio_separator_path(py_cmd)
    if not audio_separator_exe or not os.path.exists(audio_separator_exe):
        pause_and_exit(_t('err_no_exe'))

    MODEL_NAME, TARGET_STEMS = select_mode()

    os.makedirs(DRIVE_IN, exist_ok=True)
    os.makedirs(DRIVE_OUT, exist_ok=True)

    exts = ('.mp3', '.m4a', '.wav', '.m4r', '.flac', '.ogg', '.mp2', '.amr')
    files = sorted([f for f in os.listdir(DRIVE_IN) if f.lower().endswith(exts) and not f.startswith('chunk_')])

    if not files:
        pause_and_exit(_t('err_no_files', os.path.basename(DRIVE_IN)))

    v_free = shutil.disk_usage(DRIVE_OUT).free
    EXP_SZ = 30 * 1024 * 1024 
    DEV = subprocess.DEVNULL  

    print(_t('start_work', len(files), MODEL_NAME))

    for i, fn in enumerate(files):
        if v_free < EXP_SZ:
            prt(_t('err_storage'), True); break

        in_p = os.path.join(DRIVE_IN, fn)
        bn = os.path.splitext(fn)[0]
        pfx = f"[{i+1:02d}/{len(files):02d}] {fn[:15]}..."
        
        skip_file = True
        for target in TARGET_STEMS:
            check_out_p = os.path.join(DRIVE_OUT, f"{bn}_{target.capitalize()}.mp3")
            if not (os.path.exists(check_out_p) and os.path.getsize(check_out_p) > 1024):
                skip_file = False
                break
                
        if skip_file:
            prt(f"{pfx}{_t('skip_file')}", True); continue

        T_IN, T_OUT = os.path.join(TEMP_IN, bn), os.path.join(TEMP_OUT, bn)
        prt(f"{pfx}{_t('pre_process')}")
        
        shutil.rmtree(T_IN, ignore_errors=True); shutil.rmtree(T_OUT, ignore_errors=True)
        os.makedirs(T_IN, exist_ok=True); os.makedirs(T_OUT, exist_ok=True)
        
        subprocess.run([ffmpeg_exe, '-y', '-i', in_p, '-f', 'segment', '-segment_time', '120', '-c:a', 'pcm_s16le', os.path.join(T_IN, 'chunk_%03d.wav')], check=True, stdout=DEV, stderr=DEV)
        
        chks = sorted(glob.glob(os.path.join(T_IN, "chunk_*.wav")))
        if len(chks) > 1:
            lc, pc = chks[-1], chks[-2]
            if os.path.getsize(lc) < 3528000: 
                m_txt = os.path.join(T_IN, 'm.txt')
                with open(m_txt, 'w', encoding='utf-8') as f: 
                    f.write(f"file '{os.path.basename(pc)}'\nfile '{os.path.basename(lc)}'\n")
                m_nm = pc.replace('.wav', '_m.wav')
                subprocess.run([ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0', '-i', m_txt, '-c', 'copy', m_nm], check=True, stdout=DEV, stderr=DEV)
                os.remove(lc); os.remove(pc); os.rename(m_nm, pc)
                chks = sorted(glob.glob(os.path.join(T_IN, "chunk_*.wav")))

        tot = len(chks)
        for c_idx, cp in enumerate(chks):
            pct = ((c_idx + 1) / tot) * 100
            fld = int((pct / 100) * 20)
            bar = '█' * fld + '░' * (20 - fld)
            prt(f"{pfx}{_t('separating', bar, pct, c_idx+1, tot)}")

            subprocess.run([audio_separator_exe, cp, '--model_filename', MODEL_NAME, '--output_dir', T_OUT, '--output_format', 'WAV'], check=True, stdout=DEV, stderr=DEV)

        prt(f"{pfx}{_t('merging')}")
        
        for target in TARGET_STEMS:
            stems = sorted([f for f in glob.glob(os.path.join(T_OUT, "*.wav")) if target.lower() in f.lower()])
            
            if stems:
                c_txt = os.path.join(T_OUT, f'c_{target}.txt')
                with open(c_txt, 'w', encoding='utf-8') as f:
                    for sc in stems:
                        safe_path = os.path.abspath(sc).replace('\\', '/')
                        f.write(f"file '{safe_path}'\n")
                
                final_out_p = os.path.join(DRIVE_OUT, f"{bn}_{target.capitalize()}.mp3")
                subprocess.run([ffmpeg_exe, '-y', '-f', 'concat', '-safe', '0', '-i', c_txt, '-c:a', 'libmp3lame', '-b:a', '320k', final_out_p], check=True, stdout=DEV, stderr=DEV)
                
                if os.path.exists(final_out_p): v_free -= os.path.getsize(final_out_p)

        prt(f"{pfx}{_t('done')}", True)
        shutil.rmtree(T_IN, ignore_errors=True); shutil.rmtree(T_OUT, ignore_errors=True)

    pause_and_exit(_t('all_done'))

if __name__ == "__main__":
    main()
