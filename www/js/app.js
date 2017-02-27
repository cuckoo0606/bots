var App = angular.module('starter', ['ionic', 'ng-echarts', 'ngCookies', 'ionic-toast', 'starter.controllers', 'starter.services'])
App.directive('ngInput', [function () {
    return {
        restrict: 'A',
        require: '?ngModel',
        link: function(scope, element, attrs) {
            element.on('input',oninput);
            scope.$on('$destroy',function(){//销毁的时候取消事件监听
                element.off('input',oninput);
            });
            function oninput(event){
                scope.$evalAsync(attrs['ngInput'],{$event:event,$value:this.value});
            }
        }
    }
}])
.run(function($ionicPlatform, $rootScope, $state, $timeout, $ionicLoading, $ionicPopup, $http, $cookies, $location, AppConfigService) {
    $ionicPlatform.ready(function() {
        if (window.cordova && window.cordova.plugins && window.cordova.plugins.Keyboard) {
            cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
            cordova.plugins.Keyboard.disableScroll(true);
        }
        if (window.cordova && window.cordova.plugins && window.cordova.plugins.orientationLock) {
            //强制竖屏
            window.plugins.orientationLock.lock("portrait");
            //强制横屏
            //window.plugins.orientationLock.lock("landscape");
            //解除锁定
            //window.plugins.orientationLock.unlock();
        }
        if (window.StatusBar) {
            StatusBar.styleDefault();
        }
        //从Cookie读取微信信息
        AppConfigService.wx_auth.scope = $cookies.get("ws");
        AppConfigService.wx_auth.openid = $cookies.get("wo");
        AppConfigService.wx_auth.unionid = $cookies.get("wu");
        AppConfigService.wx_auth.expires_in = $cookies.get("we");
        AppConfigService.wx_auth.access_token = $cookies.get("wa");
        AppConfigService.wx_auth.refresh_token = $cookies.get("wr");
        
        $timeout(function() {
            var reg = new RegExp("(^|&)show=([^&]*)(&|$)", "i");
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                var state = unescape(r[2]);
                $state.go(state);
            }
        }, 1000);
    });
            


    //判断登陆状态
    $rootScope.$on('$stateChangeStart',function(event, toState, toParams, fromState, fromParams, options) {
        var views = [ "tab.qoute", "tab.history", "tab.profile", "tab.trade", "trade" ];

        //禁止连续点击导航栏
        if (views.indexOf(toState.name) >= 0) {
            angular.element(document.querySelectorAll('.tab-nav.tabs a')).attr("disabled", "disabled");
            $timeout(function() {
                angular.element(document.querySelectorAll('.tab-nav.tabs a')).attr("disabled", "");
            }, 300);
        }

        if (views.indexOf(toState.name) >= 0 && !$rootScope.user) {
            $state.go("signin");
            event.preventDefault();
        }
    });
    //刷新微信标题
    $rootScope.$on('$stateChangeSuccess',function(event, toState, toParams, fromState, fromParams, options) {
        var views = [ "tab.qoute", "tab.history", "tab.profile", "tab.trade", "trade" ];
        if (views.indexOf(toState.name) >= 0) {
            $timeout(function() {
                var body = angular.element(document.querySelector('body'));
                body.append("<iframe src='/favicon.ico'></iframe>");

                $timeout(function() {
                    angular.element(document.querySelector('iframe')).remove();
                }, 500);
            }, 500);
        }
    });
})

.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider, $httpProvider) {
    //解决缓存问题
    if (!$httpProvider.defaults.headers.get) {
            $httpProvider.defaults.headers.get = {}; 
    }
    $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';

    $ionicConfigProvider.platform.ios.tabs.style('standard'); 
    $ionicConfigProvider.platform.ios.tabs.position('bottom');
    $ionicConfigProvider.platform.android.tabs.style('standard');
    $ionicConfigProvider.platform.android.tabs.position('standard');

    $ionicConfigProvider.platform.ios.navBar.alignTitle('center'); 
    $ionicConfigProvider.platform.android.navBar.alignTitle('center');

    $ionicConfigProvider.platform.ios.views.transition('ios'); 
    $ionicConfigProvider.platform.android.views.transition('android');

    if (!ionic.Platform.isIOS()) {
        $ionicConfigProvider.scrolling.jsScrolling(true);
    }

    $stateProvider

    .state('signin', {
        cache: false,
        url: '/signin',
        controller: "SigninCtrl",
        templateUrl: 'templates/signin.html'
    })

    .state('install', {
        cache: false,
        url: '/install',
        templateUrl: 'templates/install.html'
    })

    .state('cpa', {
        cache: false,
        url: '/cpa',
        templateUrl: 'templates/cp-agreement.html'
    })

    .state('tpa', {
        cache: false,
        url: '/tpa',
        templateUrl: 'templates/trade-agreement.html'
    })

    .state('signup', {
        cache: false,
        url: '/signup',
        controller: "SignupCtrl",
        templateUrl: 'templates/signup.html'
    })
    
    .state('signuperweima', {
        cache: false,
        url: '/signuperweima',
        controller: "SignupCtrl",
        templateUrl: 'templates/sign-up-erweima.html'
    })

    .state('trade', {
        cache: false,
        url: '/trade/:mode/:market/:code',
        controller: "TradeCtrl",
        templateUrl: 'templates/trade.html'
    })

    .state('tab', {
        url: '/tab',
        abstract: true,
        templateUrl: 'templates/tabs.html',
    })

    .state('tab.qoute', {
        cache: false,
        url: '/qoute',
        views: {
            'tab-qoute': {
                controller: "QouteCtrl",
                templateUrl: 'templates/tab-qoute.html',
            }
        }
    })

    .state('tab.profile', {
        cache: false,
        url: '/profile',
        views: {
            'tab-profile': {
                controller: "ProfileCtrl",
                templateUrl: 'templates/tab-profile.html',
            }
        }
    })

    .state('tab.history', {
        cache: false,
        url: '/history/:index',
        views: {
            'tab-history': {
                controller: "HistoryCtrl",
                templateUrl: 'templates/tab-history.html',
            }
        }
    });

    $urlRouterProvider.otherwise('/signin');
    //$urlRouterProvider.otherwise('/install');

});
