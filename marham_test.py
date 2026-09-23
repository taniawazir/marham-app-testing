from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# ============================================================
# CONFIGURATION
# ============================================================

APPIUM_SERVER = "http://127.0.0.1:4723"

DEVICE_UDID = "192.168.2.220:42199"

APP_PACKAGE = "controllers.marham.marhammed"
APP_ACTIVITY = "controllers.marham.marhammed.MainActivity"


# ============================================================
# TEST CASE DATA
# ============================================================

test_cases = [
    ("TC01", "Valid Pakistan number", "3001234567"),
    ("TC02", "Valid UK number", "7400123456"),
    ("TC03", "Valid USA number", "2025550123"),
    ("TC04", "Valid UAE number", "501234567"),

    ("TC05", "Empty number", ""),

    ("TC06", "Alphabetic characters", "abcxyz"),
    ("TC07", "Special characters", "@#$%^&"),
    ("TC08", "Alphanumeric input", "300abc123"),

    ("TC09", "Too few digits", "12345"),
    ("TC10", "Too many digits", "300123456789999"),

    ("TC11", "Number with spaces", "300 1234567"),
    ("TC12", "Number with leading zero", "03001234567"),
    ("TC13", "International format", "+923001234567"),
]


# ============================================================
# APPIUM OPTIONS
# ============================================================

options = UiAutomator2Options()

options.platform_name = "Android"
options.automation_name = "UiAutomator2"
options.device_name = "Android"

options.udid = DEVICE_UDID

options.app_package = APP_PACKAGE
options.app_activity = APP_ACTIVITY

options.set_capability(
    "appium:ignoreHiddenApiPolicyError",
    True
)


# ============================================================
# START APPIUM
# ============================================================

driver = webdriver.Remote(
    APPIUM_SERVER,
    options=options
)

wait = WebDriverWait(driver, 15)

print("Appium connected successfully.")


# ============================================================
# HANDLE NOTIFICATION PERMISSION
# ============================================================

try:

    allow_button = driver.find_element(
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_button"
    )

    if allow_button.is_displayed():

        allow_button.click()

        print("Notification permission allowed.")

        time.sleep(2)

except Exception:

    print("Notification permission not displayed.")


# ============================================================
# GET MOBILE NUMBER FIELD
# ============================================================

def get_mobile_field():

    return wait.until(
        EC.presence_of_element_located(
            (
                AppiumBy.CLASS_NAME,
                "android.widget.EditText"
            )
        )
    )


# ============================================================
# GET CONTINUE BUTTON
# ============================================================

def get_continue_button():

    return wait.until(
        EC.presence_of_element_located(
            (
                AppiumBy.ACCESSIBILITY_ID,
                "Continue"
            )
        )
    )


# ============================================================
# ENTER MOBILE NUMBER
# ============================================================

def enter_mobile_number(number):

    field = get_mobile_field()

    field.click()

    field.clear()

    if number:

        field.send_keys(number)

    time.sleep(1)


# ============================================================
# CHECK CONTINUE BUTTON
# ============================================================

def check_continue():

    button = get_continue_button()

    return button.is_enabled()


# ============================================================
# RUN TEST CASES
# ============================================================

print("\n")
print("==========================================")
print("MARHAM MOBILE NUMBER TESTING")
print("==========================================")


results = []


for test_id, description, number in test_cases:

    print("\n------------------------------------------")

    print("Test Case:", test_id)
    print("Description:", description)
    print("Input:", number)

    try:

        # Enter number
        enter_mobile_number(number)

        # Check Continue
        continue_enabled = check_continue()

        print(
            "Continue Enabled:",
            continue_enabled
        )


        # ==========================================
        # EXPECTED RESULT
        # ==========================================

        if test_id == "TC05":

            # Empty number should disable Continue

            if not continue_enabled:

                status = "PASS"

            else:

                status = "FAIL"


        elif test_id in ["TC01", "TC02", "TC03", "TC04"]:

            # Valid numbers should enable Continue

            if continue_enabled:

                status = "PASS"

            else:

                status = "FAIL"


        else:

            # Invalid/format cases
            # Record actual behavior for analysis

            status = "OBSERVED"


        print("STATUS:", status)


        results.append(
            (
                test_id,
                description,
                number,
                continue_enabled,
                status
            )
        )


    except Exception as e:

        print("ERROR:", e)

        results.append(
            (
                test_id,
                description,
                number,
                "N/A",
                "ERROR"
            )
        )


# ============================================================
# TEST SUMMARY
# ============================================================

print("\n")
print("==========================================")
print("TEST EXECUTION SUMMARY")
print("==========================================")


for result in results:

    test_id = result[0]
    description = result[1]
    number = result[2]
    continue_enabled = result[3]
    status = result[4]

    print(
        f"{test_id} | "
        f"{description} | "
        f"Input: {number} | "
        f"Continue: {continue_enabled} | "
        f"{status}"
    )


# ============================================================
# CLOSE APP
# ============================================================

driver.quit()

print("\n")
print("==========================================")
print("TEST EXECUTION COMPLETED")
print("==========================================")