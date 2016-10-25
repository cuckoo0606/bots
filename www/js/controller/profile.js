angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce,
            UserService, OrderService, CloseOrderService, AppConfigService, CapitalService) {
    OrderService.init(function(){ });
    CloseOrderService.init(function(){ });
    
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;

    $scope.pay_modal_url = "";
    $scope.deposit_bank_list = [];
    $scope.bank_list = AppConfigService.bank_list;
    $scope.bank_info = {
        "bank": UserService.user.BankName,
        "bank_user": UserService.user.BankUserName,
        "bank_brand": UserService.user.BankAddress,
        "bank_card": UserService.user.BankAccount,
    };

    $scope.deposit = {
        "user": UserService.user.Id,
        "pay_type": "ecpss",
        "amount": 0,
        "bank": "",
        "return_url": "123",
    };

    $ionicModal.fromTemplateUrl('templates/capital-history-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.capital_history_modal = modal;
    });
    
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
        $scope.capital_deposit_modal.show();
    }

    $scope.show_withdraw_modal = function() {
        $scope.capital_withdraw_modal.show();
    }

    $scope.toggle_capital_menu = function () {
         angular.element(document.querySelectorAll("#capital-menu")).toggleClass("open");
    }

    $scope.show_bank_modal = function() {
        $scope.bank_info.bank = UserService.user.BankName;
        if($scope.bank_info.bank == "" || $scope.bank_list.indexOf($scope.bank_info.bank) < 0) {
            $scope.bank_info.bank = $scope.bank_list[0];
        }
        $scope.bank_info.bank_brand = UserService.user.BankAddress;
        $scope.bank_info.bank_user = UserService.user.BankUserName;
        $scope.bank_info.bank_card = UserService.user.BankAccount;
        $scope.bank_info_modal.show();
    }

    $scope.pay_type_change = function() {
        CapitalService.get_bank_list({
            "pay_type": $scope.deposit.pay_type,
            "success": function(status, message, list) {
                $scope.deposit_bank_list = list;
                $scope.deposit.bank = list[0];
                console.log(list[0]);
            },
            "fail": function(status, message) {
                $scope.deposit_bank_list = [];
            },
            "error": function(status, message) {
                $scope.deposit_bank_list = [];
            },
        });
    }
    $scope.pay_type_change();

    $scope.update_bank = function() {
        $ionicLoading.show({
            template: "正在操作"   
        });
        UserService.update_bank({
            "user": UserService.user.Id,
            "bank": $scope.bank_info.bank,
            "bank_user": $scope.bank_info.bank_user,
            "bank_brand": $scope.bank_info.bank_brand,
            "bank_card": $scope.bank_info.bank_card,
            "success": function(status, message, user) {
                $rootScope.user = user;
                $ionicLoading.hide();
                $scope.bank_info_modal.hide();
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

    $scope.submit_deposit = function() {
        $ionicLoading.show({
            template: "正在提交支付请求"   
        });
        
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

    $scope.order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }
});
