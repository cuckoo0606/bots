angular.module('starter.controllers')

.controller('SignupCtrl', function($scope, $rootScope, $http, $state, $timeout, $interval, $ionicHistory, $window, $ionicLoading, $ionicScrollDelegate, 
            UserService, QouteService, SMSService, AppConfigService) {
    $scope.message = "";
    $scope.is_signin = false;
    $scope.show_signup_code = AppConfigService.show_signup_code;
    $scope.users = { 
        "username": "",
        "passwd": "",
        "phone": "",
        "agree": true,
        "code": "",
        "referralcode":""
    }
    $scope.sms_remaining = 0;
    $scope.sms_btn_text = "获取验证码";
    $scope.sign_up_weixin = AppConfigService.if_weixin
    //判断当前页面是否有code，有推荐码输入框则无法修改
    var reg = new RegExp("(^|&)ref=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
    	angular.element(document.querySelectorAll(".sign_code"))[0].readOnly = true;
    	$scope.users.referralcode = unescape(r[2]);
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
        if ($scope.users.phone == "") {
            $ionicLoading.show({ template: "手机号不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.users.passwd == "") {
            $ionicLoading.show({ template: "密码不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.users.passwd != $scope.users.confirm) {
            $ionicLoading.show({ template: "两次输入密码不一致。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if (AppConfigService.show_signup_code && $scope.users.code == "") {
            $ionicLoading.show({ template: "请输入短信验证码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }
        if ($scope.users.agree == false) {
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
            "phone": $scope.users.phone, 
            "passwd": $scope.users.passwd ,
            "referralcode":$scope.users.referralcode,
            "code":$scope.users.code,
            "success": function() {
                UserService.signin({
		            "phone": $scope.users.phone,
		            "passwd": $scope.users.passwd,
		            "success": function(status, message, mess) {
                        //获取系统时间用于计算订单时间
                        UserService.request_time(function(time) {
                            var now = new Date().getTime();
                            $rootScope.server_time_tick = time - now;
                        });

                        UserService.request_user(function(user) {
                            $window.localStorage.id = user.username;
                            $rootScope.user = user;
                            $ionicHistory.clearHistory();
                            $timeout(function() {
		                		$scope.is_signin = false;
			                    $scope.spinner(false);
			                    $state.go("signuperweima");
		                	},2000);
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
                $scope.message = "该用户已注册";
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
	
	$scope.sign_in_trade = function(){
		QouteService.init(function() {
            $state.go("tab.qoute");
        });
	}
	
    $scope.get_verify = function() {
        var pattern = /1\d{10}/;
        if ($scope.users.phone == "" || !pattern.test($scope.users.phone)) {
            $ionicLoading.show({ template: "无效的手机号码。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
        }

        $ionicLoading.show({ template: "正在获取验证码" });

        SMSService.get_verify({
            "phone": $scope.users.phone,
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
