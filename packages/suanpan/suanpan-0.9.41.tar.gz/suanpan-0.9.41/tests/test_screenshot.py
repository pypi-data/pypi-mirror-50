import suanpan
from suanpan.app import app
from suanpan.app.arguments import Screenshot
from suanpan.utils import image

test_image = image.read("tests/test.png")


@app.param(Screenshot(key="outputData1", alias="screenshot"))
def test_screenshot(context):
    args = context.args
    for _ in range(10):
        args.screenshot.save(test_image)


if __name__ == "__main__":
    suanpan.run(app)
