import suanpan
from suanpan.app import app
from suanpan.arguments import String


@app.output(String(key="outputData1"))
def test_app(_):
    print("test_app")
    return "test_app"


@app.beforeInit
def test_app_before_init():
    print("app_before_init")


@app.afterInit
def test_app_after_init(_):
    print("app_after_init")


@app.beforeCall
def test_app_before_call(_):
    print("app_before_call")


@app.afterCall
def test_app_after_call(_):
    print("app_after_call")


@app.beforeSave
def test_app_before_save(_):
    print("app_before_save")


@app.afterSave
def test_app_after_save(_):
    print("app_after_save")


@app.trigger(interval=100)
@app.trigger.output(String(key="outputData1"))
def test_trigger(_):
    print("test_trigger")
    return "test_trigger"


@app.trigger.beforeInit
def test_trigger_before_init():
    print("trigger_before_init")


@app.trigger.afterInit
def test_trigger_after_init(_):
    print("trigger_after_init")


@app.trigger.beforeCall
def test_trigger_before_call(_):
    print("trigger_before_call")


@app.trigger.afterCall
def test_trigger_after_call(_):
    print("trigger_after_call")


@app.trigger.beforeSave
def test_trigger_before_save(_):
    print("trigger_before_save")


@app.trigger.afterSave
def test_trigger_after_save(_):
    print("trigger_after_save")


if __name__ == "__main__":
    suanpan.run(app)
