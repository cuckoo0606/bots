angular.module('starter', ['ionic', 'ionic-datepicker', 'echarts-ng', 'ionic-toast', 'starter.controllers', 'starter.services'])

.run(function($ionicPlatform, $rootScope, $state, $timeout, $ionicLoading, $ionicPopup, $http) {
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
    });

    //判断登陆状态
    $rootScope.$on('$stateChangeStart',function(event, toState, toParams, fromState, fromParams, options) {
        var views = [ "tab.qoute", "tab.history", "tab.profile", "trade" ];

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
        var views = [ "signin", "tab.qoute", "tab.history", "tab.profile", "trade" ];
        if (views.indexOf(toState.name) >= 0) {
            $timeout(function() {
                var body = angular.element(document.querySelector('body'));
                body.append("<iframe src='/favicon.ico'></iframe>");

                $timeout(function() {
                    angular.element(document.querySelector('iframe')).remove();
                }, 100);
            }, 100);
        }
    });
})

.config(function($stateProvider, $urlRouterProvider, $ionicConfigProvider) {

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
        url: '/signin',
        controller: "SigninCtrl",
        templateUrl: 'templates/signin.html'
    })

    .state('trade', {
        cache: false,
        url: '/trade/:qid',
        controller: "TradeCtrl",
        templateUrl: 'templates/trade.html'
    })

    .state('tab', {
        url: '/tab',
    abstract: true,
    templateUrl: 'templates/tabs.html',
    })

    .state('tab.qoute', {
        url: '/qoute',
    views: {
        'tab-qoute': {
            controller: "QouteCtrl",
    templateUrl: 'templates/tab-qoute.html',
        }
    }
    })

    .state('tab.profile', {
        url: '/profile',
    views: {
        'tab-profile': {
            controller: "ProfileCtrl",
    templateUrl: 'templates/tab-profile.html',
        }
    }
    })

    .state('tab.history', {
        url: '/history/:index',
    views: {
        'tab-history': {
            cache: false,
    controller: "HistoryCtrl",
    templateUrl: 'templates/tab-history.html',
        }
    }
    });

    $urlRouterProvider.otherwise('/signin');

});
