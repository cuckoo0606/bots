angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce,
            UserService, OrderService, LimitOrderService, CloseOrderService, AppConfigService, CapitalService) {
    OrderService.init(function(){ });
    LimitOrderService.init(function(){ });
    CloseOrderService.init(function(){ });
    
    $scope.order_list = OrderService.order_list;
    $scope.limit_order_list = LimitOrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;

    $scope.bank_list = AppConfigService.bank_list;

    $scope.bank_info = {
        "bank": UserService.user.BankName,
        "bank_user": UserService.user.BankUserName,
        "bank_brand": UserService.user.BankAddress,
        "bank_card": UserService.user.BankAccount,
    };

    if($scope.bank_list.indexOf($scope.bank_info.bank) < 0) {
        $scope.bank_info.bank = $scope.bank_list[0];
    }

    $scope.deposit = {
        "user": UserService.user.Id,
        "type": "ecpss",
        "amount": 0,
        "bank": "NOCARD",
        "return_url": "123",
    };

    $scope.pay_modal_url = "";
    $ionicModal.fromTemplateUrl('templates/pay-webview-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.pay_webview_modal = modal;
    });
    
    $ionicModal.fromTemplateUrl('templates/bank-info-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.bank_info_modal = modal;
    });

    $scope.show_bank_modal = function() {
        $scope.bank = UserService.user.BankName;
        $scope.bank_brand = UserService.user.BankAddress;
        $scope.bank_user = UserService.user.BankUserName;
        $scope.bank_card = UserService.user.BankAccount;
        $scope.bank_info_modal.show();
    }

    $scope.deposit_amount = 0;
    $scope.withdraw_amount = 0;
    $scope.pay_type = "ecpss";
    $ionicModal.fromTemplateUrl('templates/capital-deposit-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.capital_deposit_modal = modal;
    });

    $ionicModal.fromTemplateUrl('templates/capital-withdraw-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.capital_withdraw_modal = modal;
    });

    $scope.show_deposit_modal = function() {
        $scope.deposit_amount = 0;
        $scope.capital_deposit_modal.show();
    }

    $scope.show_withdraw_modal = function() {
        $scope.withdraw_amount = 0;
        $scope.capital_withdraw_modal.show();
    }

    $scope.submit_deposit = function() {
        $ionicLoading.show({
            template: "正在提交支付请求"   
        });
        console.log($scope.deposit);
        CapitalService.deposit({
            "deposit": $scope.deposit,
            "success": function(status, message, url) {
                console.log(url);
                $ionicLoading.hide();
                $scope.pay_modal_url = $sce.trustAsResourceUrl(url);
                $scope.pay_webview_modal.show();
            },
            "fail": function(status, message) {
                $ionicLoading.show({
                    template: message
                });
                $timeout(function () {
                    $ionicLoading.hide();
                }, 2000);
            },
            "error": function(status, message) {
                $ionicLoading.show({
                    template: message
                });
                $timeout(function () {
                    $ionicLoading.hide();
                }, 2000);
            },
        });
        $scope.capital_deposit_modal.hide();
    }

    $scope.withdraw = function() {
        $scope.capital_withdraw_modal.hide();
    }

    $ionicModal.fromTemplateUrl('templates/capital-history-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.capital_history_modal = modal;
    });

    $scope.order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }

    $scope.limit_order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.limit_order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }

    $scope.toggle_capital_menu = function () {
         angular.element(document.querySelectorAll("#capital-menu")).toggleClass("open");
    }
});
