import re, os, inspect, logging, datetime, sys, configparser

def exedir(mode="script"):
    """
    mode:
    - "cwd": 현재 작업 디렉토리
    - "exe": 실행 파일 디렉토리
    - "script": 스크립트 파일 디렉토리
    """
    if mode == "exe" and os.path.splitext(sys.executable)[1] == ".exe" and "python" not in sys.executable.lower():
        return os.path.dirname(sys.executable)
    elif mode == "cwd":
        return os.getcwd()
    elif mode == "script":
        return os.path.dirname(os.path.abspath(__file__))
    else:
        raise ValueError("Invalid mode. Use 'cwd', 'exe', or 'script'.")
    
def load_config(file_path=f"{exedir("script")}\\.env"):
    config = configparser.ConfigParser()
    config.optionxform = str  # 키 이름의 대소문자 구분 유지

    # UTF-8 인코딩으로 파일 읽기
    config.read(file_path, encoding="utf-8")
    # 모든 섹션과 항목을 동적으로 읽어서 딕셔너리로 변환
    config_data = {}
    for section in config.sections():
        config_data[section] = {}
        for key in config[section]:
            # Boolean 값인 경우 처리
            if config[section][key].lower() in ['true', 'false']:
                config_data[section][key] = config.getboolean(section, key)
            else:
                config_data[section][key] = config.get(section, key)
    return config_data