angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce, $ionicHistory,
            UserService, OrderService, CloseOrderService, AppConfigService, CapitalService) {
            	
    $scope.qrcode_url = AppConfigService.get_erweima_url + AppConfigService.erweima_url + "%23/signup?code=" + $rootScope.user.referee;
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;
	$scope.account = $rootScope.user;
    $scope.pay_modal_url = "";
    $scope.deposit_bank_list = [];
    $scope.moneyList=[];
    $scope.bank_list = AppConfigService.bank_list;
    $scope.type_list = AppConfigService.type_list;
    $scope.footshow={
    	none:true
    };
    $scope.user_bank={
    	name:"",
    	code:""
    };
    $scope.judge_bank_value=false;
    $scope.user_info = {
        "id_card": "",
        "bank": "",
        "bank_user": "",
        "bank_brand": "",
        "bank_card": "",
    };
	$scope.choseDate={
		"startDate":"",
		"startDate":""
	};
	$scope.outAmount={
		"outamount":""
	};
    $scope.deposit = {
        "pay_type": "ecpss",
        "amount": 100,
        "bank": "",
        "body": "WECHAT RECHARGE"
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
    
    $ionicModal.fromTemplateUrl('templates/user-info-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.user_info_modal = modal;
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

	$scope.get_user_bank = function(){
		
	}
    $scope.show_user_modal = function() {
    	$ionicHistory.clearHistory();
    	$scope.user_bank=$scope.bank_list.filter(function(obj){
    		if(obj.code==$rootScope.user.bank){
    			return obj;
    		}
    	});
        $scope.user_info.bank = $scope.user_bank[0];
        if($scope.user_info.bank == "" || $scope.bank_list.indexOf($scope.user_info.bank) < 0) {
            $scope.user_info.bank = $scope.bank_list[0];
        }
        $scope.user_info.id_card = $rootScope.user.idcard;
        $scope.user_info.bank_brand = $rootScope.user.bankbranch;
        $scope.user_info.bank_user = $rootScope.user.bankholder;
        $scope.user_info.bank_card = $rootScope.user.bankaccount;
        $scope.user_info_modal.show();
    }

	$scope.show_money_list_footer = function() {
		var article_list = document.getElementsByTagName("article");
		var clickshow_list = document.getElementsByClassName("clickshow");
		for (var i=0;i<article_list.length;i++){
			if(i==this.$index){
				if(article_list[i].style.display=="block"){
					clickshow_list[i].className="icon clickshow ion-ios-arrow-up";
					article_list[i].style.display="none";
				}else {
					clickshow_list[i].className="icon clickshow ion-ios-arrow-down";
					article_list[i].style.display="block";
				}
			}else{
				article_list[i].style.display="none";
			}
		}
    }
	
    $scope.pay_type_change = function() {
        CapitalService.get_bank_list(function(list) {
            $scope.deposit_bank_list = list;
            $scope.deposit.bank = list[0];
        });
    }
    $scope.pay_type_change();
    $scope.update_user = function() {
        $ionicLoading.show({
            template: "正在操作"   
        });
        
        UserService.update_user({
        	"name": $rootScope.user.name,
        	"sex": $rootScope.user.sex,
        	"phone": $rootScope.user.phone,
        	"address": $rootScope.user.address,
        	"email": $rootScope.user.email,
        	"id_card": $scope.user_info.id_card,
            "bank": $scope.user_info.bank.code,
            "bankholder": $scope.user_info.bank_user,
            "bankbranch": $scope.user_info.bank_brand,
            "bankaccount": $scope.user_info.bank_card,
            "success": function(status, message, protocol) {
                UserService.request_user(function(user) {
                    $rootScope.user = user;
                    $ionicLoading.hide();
                    $scope.user_info_modal.hide();
                });
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
        if ($scope.deposit.amount == "" || $scope.deposit.amount == "0")  {
            $ionicLoading.show({
                template: "无效的金额"
            });

            $timeout(function () {
                $ionicLoading.hide();
            }, 2000);

            return;
        }

        $ionicLoading.show({
            template: "正在提交"
        });
        
        CapitalService.deposit_hc({
            "deposit": $scope.deposit,
            "success": function(url) {
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
        if ($scope.outAmount.outamount == "" || $scope.outAmount.outamount == "0")  {
            $ionicLoading.show({
                template: "无效的金额"
            });

            $timeout(function () {
                $ionicLoading.hide();
            }, 2000);

            return;
        }
		var judge_bank_value = false;
		(function(){
			for(var i=0;i<$scope.bank_list.length;i++){
				if(($rootScope.user.bankaccount!="")&&($rootScope.user.bankbranch!="")&&($rootScope.user.bankholder!="")&& ($rootScope.user.bank==$scope.bank_list[i].code||$rootScope.user.bank==$scope.bank_list[i].name)){
					judge_bank_value=true;
					return judge_bank_value;
				}else{
					judge_bank_value=false;
				}
			}
			return judge_bank_value;
		})();

        if(judge_bank_value){
        	$ionicLoading.show({
            template: "正在提交"
	        });
	    	
	        CapitalService.out_withdraw({
	        	"outamount": $scope.outAmount.outamount,
	        	"success": function(protocol) {
	                if (protocol.error) {
	                    $ionicLoading.show({
	                        template: protocol.error_message
	                    });
	
	                    $timeout(function() {
	                        $ionicLoading.hide();
	                    }, 3000);
	                }
	                else {

	                    $rootScope.user.amount = $scope.account.amount - $scope.outAmount.outamount;
	                    $ionicLoading.show({
	                        template: "提交成功"
	                    });
	                    $timeout(function() {
	                    $ionicLoading.hide();
	                    $scope.capital_withdraw_modal.hide();
	                	}, 1000);
	                }
	          	},
	        	"fail": function(message) {
	                $ionicLoading.show({
	                    template: message
	                });
	
	                $timeout(function() {
	                    $ionicLoading.hide();
	                }, 3000);
	          	},
	        	"error": function(message) {
	                $ionicLoading.show({
	                    template: message
	                });
	
	                $timeout(function() {
	                    $ionicLoading.hide();
	                }, 3000);
	          	}
	        });
        }else{
        	$ionicLoading.show({
            template: "银行签约信息不全。请前往个人--个人资料处编辑银行卡信息。"
	        });
	        $timeout(function () {
                $ionicLoading.hide();
            }, 2000);
        }
        
    }

    $scope.order_quantity_sum = function() {
        var sum = 0;
        angular.forEach($scope.order_list, function(value) {
            sum += value.Quantity;
        });
        return sum;
    }
    
    //用户输入银行卡号必须为数字
    $scope.only_number = function(){
    	if((event.keyCode<48||event.keyCode>57)&&(event.keyCode<96||event.keyCode>105)&&(event.keyCode!=8)){
    		event.preventDefault();
    	}
    }
    
    $scope.show_money_list = function(){
        CapitalService.request_capital_list({
        	"startDate":moment().toJSON().substring(0,10),
        	"overDate":$scope.choseDate.overDate,
        	"size":1000,
        	"page":1,
        	"success": function(message) {
        		message.forEach(function(servicevalue){
        			$scope.type_list.filter(function(arr){
        				if(servicevalue.type==arr.value){
        					$scope.moneyList.push({
		                        "_id": servicevalue._id,
		                        "remark": servicevalue.remark,
		                        "yearTime": moment(servicevalue.created).format().substring(0,10),
		                        "dayTime": moment(servicevalue.created).format().substring(11,19),
		                        "amount": servicevalue.amount,
		                        "user": servicevalue.user,
		                        "balance": servicevalue.balance,
		                        "type": servicevalue.type,
		                        "typename":arr.name
		                    });
        				}
        			});
        		});
          	}
        });
    }
    
    $scope.$on('$destroy', function() {
        $scope.user_info_modal.hide();
        $scope.capital_history_modal.hide();
        $scope.pay_webview_modal.hide();
        $scope.capital_deposit_modal.hide();
        $scope.capital_withdraw_modal();
    });
});
