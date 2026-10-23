import json
import urllib.request
from pathlib import Path


# ==========================================
# GitHub video.json 주소
# ==========================================

URL = "https://raw.githubusercontent.com/H2HCHIVE/H2HCHIVE/main/video.json"


# ==========================================
# 멤버 이름 → 파일 이름
# ==========================================

MEMBERS = {
    "지우": "jiwoo.json",
    "카르멘": "carmen.json",
    "유하": "yuha.json",
    "스텔라": "stella.json",
    "주은": "jueun.json",
    "에이나": "aina.json",
    "이안": "ian.json",
    "예온": "yeon.json"
}


# ==========================================
# video.json 다운로드
# ==========================================

print("video.json 다운로드 중...")

with urllib.request.urlopen(URL) as response:
    data = json.loads(response.read().decode("utf-8"))


print(f"총 영상 수: {len(data)}개")


# ==========================================
# 분류할 공간
# ==========================================

group_videos = []

member_videos = {
    member: []
    for member in MEMBERS
}


# ==========================================
# 그룹 / 멤버 분리
# ==========================================

for video in data:

    member = video.get("member")


    # -----------------------------
    # member가 없으면 그룹 직캠
    # -----------------------------

    if not member:

        group_videos.append(video)

        continue


    # -----------------------------
    # 멤버 직캠
    # -----------------------------

    if member in member_videos:

        # 원본 복사
        clean_video = video.copy()

        # member 필드 제거
        clean_video.pop("member", None)

        member_videos[member].append(clean_video)

    else:

        print(
            f"⚠️ 등록되지 않은 멤버 발견: {member}"
        )


# ==========================================
# JSON 저장 함수
# ==========================================

def save_json(filename, videos):

    path = Path(filename)

    with path.open(
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            videos,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"생성 완료: {filename} "
        f"({len(videos)}개)"
    )


# ==========================================
# 파일 생성
# ==========================================

save_json(
    "group.json",
    group_videos
)


for member, filename in MEMBERS.items():

    save_json(
        filename,
        member_videos[member]
    )


# ==========================================
# 검증
# ==========================================

member_total = sum(
    len(videos)
    for videos in member_videos.values()
)

total_after_split = (
    len(group_videos)
    + member_total
)


print()
print("=" * 40)
print("분리 결과")
print("=" * 40)

print(f"원본 영상 수 : {len(data)}")
print(f"그룹 직캠    : {len(group_videos)}")
print(f"멤버 직캠    : {member_total}")
print(f"분리 후 합계 : {total_after_split}")


if len(data) == total_after_split:

    print()
    print("✅ 검증 완료!")
    print("영상 누락 없이 모두 분리되었습니다.")

else:

    print()
    print("❌ 영상 수가 맞지 않습니다.")
    print("분리 과정에서 문제가 발생했습니다.")