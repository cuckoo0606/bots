angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce,
            UserService, OrderService, CloseOrderService, AppConfigService, CapitalService) {
	$('#code').qrcode({
		render:"canvas",
		width:250,
		height:250,
		text:AppConfigService.erweima_url+"/#/signup?code="+$rootScope.user.referee
	});
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;
	$scope.account = $rootScope.user;
    $scope.pay_modal_url = "";
    $scope.deposit_bank_list = [];
    $scope.moneyList=[];
    $scope.bank_list = AppConfigService.bank_list;
    $scope.bank_info = {
        "bank": UserService.user.BankName,
        "bank_user": UserService.user.BankUserName,
        "bank_brand": UserService.user.BankAddress,
        "bank_card": UserService.user.BankAccount,
        "id_card":""
    };
	$scope.choseDate={
		"startDate":"",
		"startDate":""
	};
	$scope.outAmount={
		"outamount":""
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
        	"name":$scope.account.name,
        	"sex":$scope.account.sex,
        	"phone":$scope.account.phone,
        	"address":$scope.account.address,
        	"email":$scope.account.email,
        	"id_card":$scope.account.id_card,
            "bank": $scope.bank_info.bank,
            "bankholder": $scope.bank_info.bank_user,
            "bankbranch": $scope.bank_info.bank_brand,
            "bankaccount": $scope.bank_info.bank_card,
            "success": function() {
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

    $scope.out_withdraw = function() {
    	$ionicLoading.show({
		            template: "成功提交请求"   
		        });
    	CapitalService.out_withdraw({
        	"outamount":$scope.outAmount.outamount,
        	"success": function(message) {
        		$ionicLoading.hide();
        		$rootScope.user.amount=$scope.account.amount-message.amount;
        		$scope.capital_withdraw_modal.hide();
          	}
        });
        
        
    }

    $scope.order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }
    
    $scope.show_money_list = function(){
        CapitalService.request_capital_list({
        	"startDate":$scope.choseDate.startDate,
        	"overDate":$scope.choseDate.overDate,
        	"success": function(message) {
        		message.forEach(function(value){
//      			if(value.remark=="订单到期获利结算"){
//      				value.remark=value.remark.substring(6,8);
//      			};
        			$scope.moneyList.push({
                        "_id": value._id,
                        "remark": value.remark,
                        "yearTime": value.created.substring(0,10),
                        "dayTime": value.created.substring(11,19),
                        "amount": value.amount,
                        "user": value.user,
                        "balance": value.balance,
                        "type": value.type,
                    });
        		});
          	}
        });
    }
});
