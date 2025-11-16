*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  matti
    Set Password  katti1234
    Set Password Confirmation  katti1234
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ma
    Set Password  katti1234
    Set Password Confirmation  katti1234
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  matti
    Set Password  katti1
    Set Password Confirmation  katti1
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Username  matti
    Set Password  mattionkatti
    Set Password Confirmation  mattionkatti
    Click Button  Register
    Register Should Fail With Message  Password must must contain both letters and numbers

Register With Nonmatching Password And Password Confirmation
    Set Username  matti
    Set Password  katti1234
    Set Password Confirmation  katti2345
    Click Button  Register
    Register Should Fail With Message  Passwords do not match

Register With Username That Is Already In Use
    Set Username  matti
    Set Password  katti1234
    Set Password Confirmation  katti1234
    Click Button  Register
    Register Should Succeed
    Go To Register Page
    Set Username  matti
    Set Password  mattionkatti1
    Set Password Confirmation  mattionkatti1
    Click Button  Register
    Register Should Fail With Message  User with username matti already exists

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Go To Register Page
