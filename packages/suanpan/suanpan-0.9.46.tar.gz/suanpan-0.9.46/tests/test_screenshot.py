import suanpan
from suanpan.app import app
from suanpan.app.arguments import String
from suanpan.screenshot import screenshot
from suanpan.utils import image

test_image = image.read("tests/test.png")


@app.afterInit
def clean_screenshot(_):
    screenshot.clean()


@app.param(String(key="param1"))
def test_screenshot(_):
    for _ in range(10):
        screenshot.save(test_image)


if __name__ == "__main__":
    suanpan.run(app)
