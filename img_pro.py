from PIL import Image
import numpy as np

def change_color_and_make_transparent(input_path, output_path, target_hex, tolerance=240):
    """
    이미지의 흰색 부분을 투명하게 만들고, 비흰색 부분을 원하는 색상으로 변경하는 함수
    
    :param input_path: 원본 이미지 경로
    :param output_path: 저장할 이미지 경로 (투명도를 위해 반드시 .png 확장자 사용)
    :param target_hex: 적용할 색상의 헥스 코드 (예: '#FF5733')
    :param tolerance: 흰색으로 인식할 RGB 임계값 (0~255). 기본값 240.
    """
    
    # 1. 이미지 로드 및 RGBA 모드로 변환 (투명도 처리를 위해 A채널 추가)
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)
    
    # R, G, B, A 채널 분리
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # RGB 값이 모두 tolerance(임계값) 이상이면 흰색으로 간주하는 마스크 생성
    # (완벽한 흰색인 255만 잡으면 화질 손실로 인한 옅은 회색이 남을 수 있어 임계값을 줍니다)
    white_mask = (r >= tolerance) & (g >= tolerance) & (b >= tolerance)
    
    # 헥스 코드를 RGB 값으로 변환 ('#FF0000' -> 255, 0, 0)
    target_hex = target_hex.lstrip('#')
    tr, tg, tb = tuple(int(target_hex[i:i+2], 16) for i in (0, 2, 4))
    
    # 마스크가 False인 부분(~white_mask)에 타겟 RGB 값과 완전 불투명(255) 적용
    data[~white_mask] = [tr, tg, tb, 255]
    
    # 마스크가 True인 부분(white_mask)의 Alpha(투명도) 값을 0으로 설정
    data[white_mask] = [255, 255, 255, 0] 
    
    # 배열을 다시 이미지로 변환 후 저장
    result_img = Image.fromarray(data)
    result_img.save(output_path, format="PNG")
    print(f"✅ 변환 완료! '{output_path}' 파일이 생성되었습니다.")

# === 실행 예시 ===
if __name__ == "__main__":
    # 원본 파일 이름, 저장할 파일 이름, 원하는 색상 코드(예: 흰색)
    input_file = "sample.jpg"    # 준비하신 이미지 파일 이름으로 변경하세요.
    output_file = "result.png"   # 투명 배경을 위해 반드시 png로 설정하세요.
    my_color = "#FFFFFF"         # 적용하고 싶은 색상의 헥스 코드
    
    change_color_and_make_transparent(input_file, output_file, my_color)