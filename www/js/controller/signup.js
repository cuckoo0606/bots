angular.module('starter.controllers')

.controller('SignupCtrl', function($scope, $rootScope, $http, $state, $timeout, $interval, $ionicHistory, $window, $ionicLoading, $ionicScrollDelegate, 
            UserService, QouteService, SMSService, AppConfigService) {
    $scope.message = "";
    $scope.is_signin = false;
    $scope.show_signup_code = AppConfigService.show_signup_code;
    $scope.user = { 
        "username": "",
        "passwd": "",
        "phone": "",
        "agree": true,
        "code": "",
        "referralcode":""
    }
    $scope.sms_remaining = 0;
    $scope.sms_btn_text = "获取验证码";
    //判断当前页面是否有code，有推荐码输入框则无法修改
    $scope.url=window.location.href;
    if($scope.url.indexOf("tuijianma")>0){
    	angular.element(document.querySelectorAll(".sign_code"))[0].readOnly=true;
    	$scope.user.referralcode=$scope.url.substring($scope.url.indexOf("tuijianma")+10,$scope.url.length);
    }
	
    $scope.spinner = function(visible) {
        if (visible) {
            angular.element(document.querySelectorAll(".spinner-view")).removeClass("hide");
            $timeout(function() {
                angular.element(document.querySelectorAll(".spinner-view")).addClass("open");
            }, 0);
        }
        else {
            angular.element(document.querySelectorAll(".spinner-view")).removeClass("open");
            $timeout(function() {
                angular.element(document.querySelectorAll(".spinner-view")).addClass("hide");
            }, 300);
        }
    }; 

    $scope.signup = function() {
        if ($scope.user.phone == "") {
            $ionicLoading.show({ template: "手机号不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.passwd == "") {
            $ionicLoading.show({ template: "密码不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.passwd != $scope.user.confirm) {
            $ionicLoading.show({ template: "两次输入密码不一致。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if (AppConfigService.show_signup_code && $scope.user.code == "") {
            $ionicLoading.show({ template: "请输入短信验证码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.user.agree == false) {
            $ionicLoading.show({ template: "请阅读并同意协议。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }

        $ionicScrollDelegate.scrollTop(false);
        $scope.is_signin = true;
        $scope.spinner(true);
        UserService.signup({
            "phone": $scope.user.phone, 
            "passwd": $scope.user.passwd ,
            "referralcode":$scope.user.referralcode,
            "code":$scope.user.code,
            "success": function() {
                UserService.signin({
		            "phone": $scope.user.phone,
		            "passwd": $scope.user.passwd,
		            "success": function(status, message, user) {
                        //获取系统时间用于计算订单时间
                        UserService.request_time(function(time) {
                            var now = new Date().getTime();
                            $rootScope.server_time_tick = time - now;
                        });

                        UserService.request_user(function(user) {
                            $window.localStorage.id = $scope.phone;
                            $rootScope.user = user;
                            $ionicHistory.clearHistory();

                            QouteService.init(function() {
                                $scope.is_signin = false;
                                $scope.spinner(false);
                                $state.go("tab.qoute");
                            });
                        });
		            },
		            "fail": function(status, message) {
		                $scope.message = message;
		                $timeout(function() {
		                    $scope.message = "";
		                    $scope.spinner(false);
		                    $scope.is_signin = false;
		                }, 2000);
		            },
		            "error": function(status, message) {
		                $scope.message = message;
		                $timeout(function() {
		                    $scope.message = "";
		                    $scope.spinner(false);
		                    $scope.is_signin = false;
		                }, 2000);
		            },
		        });
            },
            "fail": function(status, message) {
                $scope.message = message;
                $timeout(function() {
                    $scope.message = "";
                    $scope.spinner(false);
                    $scope.is_signin = false;
                }, 2000);
            },
            "error": function(status, message) {
                $scope.message = message;
                $timeout(function() {
                    $scope.message = "";
                    $scope.spinner(false);
                    $scope.is_signin = false;
                }, 2000);
            },
        });
    }

    $scope.get_verify = function() {
        var pattern = /1\d{10}/;
        if ($scope.user.phone == "" || !pattern.test($scope.user.phone)) {
            $ionicLoading.show({ template: "无效的手机号码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }

        $ionicLoading.show({ template: "正在获取验证码" });

        SMSService.get_verify({
            "phone": $scope.user.phone,
            "success": function() {
                $ionicLoading.hide();
                $scope.sms_remaining = 60;

                var stop = $interval(function() {
                    if($scope.sms_remaining > 0) {
                        $scope.sms_remaining = $scope.sms_remaining - 1;
                        $scope.sms_btn_text = "重新获取(" + $scope.sms_remaining + ")";
                    }
                    else {
                        $scope.sms_btn_text = "获取验证码";
                        $interval.cancel(stop); 
                    }
                }, 1000);
            },
            "fail": function(status, message) {
                $ionicLoading.show({ template: message });
                $timeout(function() {
                    $ionicLoading.hide();
                }, 3000);
            },
            "error": function(status, message) {
                $ionicLoading.show({ template: message });
                $timeout(function() {
                    $ionicLoading.hide();
                }, 3000);
            },
        });
    }
});
