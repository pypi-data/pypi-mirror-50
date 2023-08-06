from vk import Session


class CaptchedSession(Session):
    def get_captcha_key(self, captcha_image_url: str) -> str:
        captcha_key = input(f"Captcha required with url: {captcha_image_url}: ")

        return captcha_key
