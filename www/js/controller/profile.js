angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce, $ionicHistory,$filter,
            UserService, OrderService, CloseOrderService, AppConfigService, CapitalService) {
    $scope.qrcode_url = AppConfigService.get_erweima_url + escape(AppConfigService.erweima_url + "?show=signup&ref=" + $rootScope.user.referee + "#/signup");
    $scope.order_list = OrderService.order_list;
    $scope.close_order_list = CloseOrderService.order_list;
    $scope.pay_modal_url = "";
    $scope.pay_qrcode_url = "";
    $scope.money_fee = {
    	"outmoney_bank_card":"",
    	"outmoney_bank":"",
    	"outmoney_fee_type":"",
    	"outmoney_fee":"",
    	"outmoneymin":"",
    	"outmoneymax":"",
    	"inmoney_fee_type":"",
    	"inmoney_fee":"",
    	"inmoneymin":""
    };
    $scope.moneyList=[];
    $scope.has_more_money_order = {
    	if_has_more_money_order:false,
    };
    $scope.money_page_index = 0;
    $scope.deposit_bank_list = AppConfigService.deposit_bank_list;
    $scope.pay_type_list = AppConfigService.pay_type_list;
    $scope.bank_list = AppConfigService.bank_list;
    $scope.type_list = AppConfigService.type_list;
    $scope.pay_bank_list = [];
	$scope.change_userpass={
		oldpass:"",
		newpass:"",
		newpassangin:""
	};
    $scope.footshow={
    	none:true
    };
    $scope.user_bank={
    	"userbankmes":"",
    };
    $scope.user_bank.userbankmes=$scope.bank_list.filter(function(obj){
		if(obj.code==$rootScope.user.bank||obj.name==$rootScope.user.bank){
			return obj;
		}
	});
    $scope.judge_bank_value=false;
    $scope.user_info = {
        "id_card": "",
        "bank": {},
        "bank_user": "",
        "bank_brand": "",
        "bank_card": "",
    };
	$scope.choseDate={
		"startDate":"",
		"endDate":""
	};
	$scope.outAmount={
		"outamount":"",
	};
    $scope.deposit = {
        "pay_type": AppConfigService.default_pay_type,
        "amount": 100,
        "body": "WECHAT RECHARGE",
        "openid": AppConfigService.wx_auth.openid,
        "user": $rootScope.user_id,
    };
    $scope.inmoneybank={
    	'bankmes' : ''
    };
    $scope.pay_shangyinxin_mes = {
		'bankcard':'4367423328020566868',
		'usercard':'445221198606285617',
		'phone':'13430253813',
		'name':'林博',
		'success':true
    };
    $scope.pay_shangyinxin_pay = {
    	'surecode':"",
    	'surelistid':'',
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
    
    $ionicModal.fromTemplateUrl('templates/pay-qrcode-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.pay_qrcode_modal = modal;
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
    
    $ionicModal.fromTemplateUrl('templates/user-change-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.user_change_modal = modal;
    });

    $ionicModal.fromTemplateUrl('templates/pay-money-modal.html', {
        scope: $scope,
        animation: 'slide-in-up'
    }).then(function(modal) {
        $scope.pay_money_modal = modal;
    });
    
	//入金界面
    $scope.show_deposit_modal = function() {
    	$scope.capital_deposit_modal.show();
    	
		if($scope.pay_type_list.indexOf("huichao") !=-1 ){
			$scope.pay_bank_list = $scope.deposit_bank_list.filter(function(value){
				if(value.HCcode){
					return value;
				}
			});
		}else if($scope.pay_type_list.indexOf("huanxun") !=-1 ){
			$scope.pay_bank_list = $scope.deposit_bank_list.filter(function(value){
				if(value.HYcode){
					return value;
				}
			});
		}else if($scope.pay_type_list.indexOf("shangxin") !=-1 ){
			$scope.pay_bank_list = $scope.deposit_bank_list.filter(function(value){
				if(value.SXcode){
					return value;
				}
			});
		};
		if($rootScope.user.bank){
			var defalutobj = $scope.deposit_bank_list.filter(function(value){
				if($rootScope.user.bank == value.name || $rootScope.user.bank == value.code){
					return value;
				}
			});
			$scope.inmoneybank.bankmes = defalutobj[0];
		}else if($rootScope.user.bank==''||!$rootScope.user.bank){
			$scope.inmoneybank.bankmes = $scope.pay_bank_list[0];
		}
		
        CapitalService.system_config({
        	"type":"income-handling-type",
			"success":function(value){
				$scope.money_fee.inmoney_fee_type = value;
				if(value == 0){
					CapitalService.system_config({
						"type":"income-handling-percent",
						"success":function(value){
							$scope.money_fee.inmoney_fee = parseFloat(value);
						},
						"error":function(status,message){
							$scope.money_fee.inmoney_fee = 0;
						}
					})
				}else if(value == 1){
					CapitalService.system_config({
						"type":"income-handling-amount",
						"success":function(value){
							$scope.money_fee.inmoney_fee = parseFloat(value);
						},
						"error":function(status,message){
							$scope.money_fee.inmoney_fee = 0;
						}
					})
				}
			},
			"error":function(status,message){
				$scope.money_fee.inmoney_fee = 0;
				$scope.money_fee.inmoney_fee_type = 0;
			}
		});
		CapitalService.system_config({
        	"type":"income-least-amount",
			"success":function(value){
				$scope.money_fee.inmoneymin = value;
			},
			"error":function(status,message){
				$scope.money_fee.inmoneymin = 0;
			}
		});
    }

	//入金接口
    $scope.submit_deposit = function() {
        if ($scope.deposit.amount == "" || $scope.deposit.amount == "0"||$scope.deposit.amount == "undefined")  {
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
        
        var fail = function(status, message) {
            $ionicLoading.show({
                template: message
            });
            $timeout(function () {
                $ionicLoading.hide();
            }, 2000);
        }

        var error = function(status, message) {
            $ionicLoading.show({
                template: message
            });
            $timeout(function () {
                $ionicLoading.hide();
            }, 2000);
        }
       
        if ($scope.deposit.pay_type == "huichao") { 
            CapitalService.deposit_hc({
                "deposit": $scope.deposit,
                "bankcode":$scope.inmoneybank.bankmes.HCcode,
                "success": function(url) {
                    $ionicLoading.hide();
                    $scope.capital_deposit_modal.hide();
                    $scope.pay_modal_url = $sce.trustAsResourceUrl(url);
                    $scope.pay_webview_modal.show();
                },
                "fail": fail,
                "error": error,
            });
        }
        else if($scope.deposit.pay_type == "shangxin") {
        	$timeout(function () {
	        	$ionicLoading.hide();
	        	$scope.capital_deposit_modal.hide();
		        $scope.pay_money_modal.show();
		        $scope.pay_shangyinxin_mes.success = true;
            }, 1000);
	    }
        else if($scope.deposit.pay_type == "zhongyun") {
	         CapitalService.deposit_zhongyun({
	            "deposit": $scope.deposit,
	            "success": function(url) {
	                $ionicLoading.hide();
                    $scope.capital_deposit_modal.hide();
                    $scope.pay_modal_url = $sce.trustAsResourceUrl(url);
                    $scope.pay_webview_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "zhongyun_wecat") {
	         CapitalService.deposit_zhongyun_wecat({
	            "deposit": $scope.deposit,
	            "success": function(url) {
	            	$ionicLoading.hide();
	                $scope.capital_deposit_modal.hide();
	                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(url);
	                $scope.pay_qrcode_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "huanxun") {
	         CapitalService.deposit_hx({
	            "deposit": $scope.deposit,
	            "bankcode":$scope.inmoneybank.bankmes.HYcode,
	            "success": function(url) {
	                $ionicLoading.hide();
                    $scope.capital_deposit_modal.hide();
                    $scope.pay_modal_url = $sce.trustAsResourceUrl(url);
                    $scope.pay_webview_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "huanxun_wecat") {
	         CapitalService.deposit_hxwecat({
	            "deposit": $scope.deposit,
	            "success": function(url) {
	                $ionicLoading.hide();
	                $scope.capital_deposit_modal.hide();
	                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(url);
	                $scope.pay_qrcode_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "zhihui") {
	         CapitalService.deposit_zhihui({
	            "deposit": $scope.deposit,
	            "txnType":"",
	            "payType":"",
	            "bankcode":$scope.inmoneybank.bankmes.ZHcode,
	            "success": function(url) {
	                $ionicLoading.hide();
                    $scope.capital_deposit_modal.hide();
                    $scope.pay_modal_url = $sce.trustAsResourceUrl(url);
                    $scope.pay_webview_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "zhihui_wecat") {
	         CapitalService.deposit_zhihui({
	            "deposit": $scope.deposit,
	            "txnType":"",
	            "payType":"",
	            "success": function(url) {
	                $ionicLoading.hide();
	                $scope.capital_deposit_modal.hide();
	                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(url);
	                $scope.pay_qrcode_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "weifutong") {
	         CapitalService.deposit_swift({
	            "deposit": $scope.deposit,
	            "success": function(url) {
	                $ionicLoading.hide();
	                $scope.capital_deposit_modal.hide();
	                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(url);
	                $scope.pay_qrcode_modal.show();
	            },
	            "fail": fail,
	            "error": error,
	        });
	    }
        else if($scope.deposit.pay_type == "wechat") {
            CapitalService.deposit_wechat({
                "deposit": $scope.deposit,
                "success": function(code, msg, res) {
                    $ionicLoading.hide();

                    wx.config({
                        debug: false,
                        appId: res.config.appId,
                        timestamp: res.config.timestamp,
                        nonceStr: res.config.nonceStr,
                        signature: res.config.signature,
                        jsApiList: [ "chooseWXPay" ]
                    });

                    wx.ready(function(){
                        wx.chooseWXPay({
                            timestamp: res.payinfo.timeStamp,
                            nonceStr: res.payinfo.nonceStr,
                            package: res.payinfo.package,
                            signType: res.payinfo.signType,
                            paySign: res.payinfo.paySign,
                            success: function () {
                                $scope.capital_deposit_modal.hide();
                            }
                        });
                    });
                },
                "fail": fail,
                "error": error,
            });
        }
    }
	//商信第一步
    $scope.pay_shangyinxin = function(){
         CapitalService.deposit_shangyin_mes({
            "deposit": $scope.deposit,
            "bankCard" :$scope.pay_shangyinxin_mes.bankcard,
			"cardId":$scope.pay_shangyinxin_mes.usercard,
			"phone":$scope.pay_shangyinxin_mes.phone,
			"realName":$scope.pay_shangyinxin_mes.name,
            "bankId":$scope.inmoneybank.bankmes.SXcode,
            "success": function(mes) {
                console.log(mes);
                $scope.pay_shangyinxin_pay.surelistid = mes.no;
                $scope.pay_shangyinxin_mes.success = false;
            },
            "fail": function(status, message) {
	            $ionicLoading.show({
	                template: "银行信息错误"
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
	                $scope.pay_shangyinxin_mes.success = false;
	            }, 2000);
	        },
        });
    }
    //商信第二步
    $scope.sure_pay_shangyinxin = function(){
         CapitalService.deposit_shangyin_sure({
            "no": $scope.pay_shangyinxin_pay.surelistid,
            "verifyCode" :pay_shangyinxin_pay.surecode,
            "success": function(url) {
                console.log(url);
	            $ionicLoading.show({
	                template: "入金成功"
	            });
	            $timeout(function () {
	                $ionicLoading.hide();
	            }, 2000);
            },
            "fail": function(status, message) {
	            $ionicLoading.show({
	                template: "提交失败"
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
	                $scope.pay_shangyinxin_mes.success = false;
	            }, 2000);
	        },
        });
    }
	//出金页面
    $scope.show_withdraw_modal = function() {
        $scope.capital_withdraw_modal.show();
        $scope.money_fee.outmoney_bank_card = "";
        $scope.money_fee.outmoney_bank_card_icon = "";
        if($rootScope.user.bankaccount){
        	var bank_lengths = [4,10,16,22];
        	for(var i=0;i<($rootScope.user.bankaccount.length - $rootScope.user.bankaccount.length % 4);i++){
        		$scope.money_fee.outmoney_bank_card = $scope.money_fee.outmoney_bank_card+'*';
        		if(bank_lengths.indexOf($scope.money_fee.outmoney_bank_card.length) != -1){
        			$scope.money_fee.outmoney_bank_card = $scope.money_fee.outmoney_bank_card+'  ';
        		}
        	};
        	$scope.money_fee.outmoney_bank_card = $scope.money_fee.outmoney_bank_card + $rootScope.user.bankaccount.substring($rootScope.user.bankaccount.length - $rootScope.user.bankaccount.length % 4);
        	$scope.money_fee.outmoney_bank = $scope.deposit_bank_list.filter(function(value){
				if([value.name,value.code,value.codenumber].indexOf($rootScope.user.bank)!=-1){
					return value;
				}
			});
			
        };
        
        CapitalService.system_config({
        	"type":"pay-handling-type",
			"success":function(value){
				$scope.money_fee.outmoney_fee_type = value;
				if(value == 0){
					CapitalService.system_config({
						"type":"pay-handling-percent",
						"success":function(value){
							$scope.money_fee.outmoney_fee = parseFloat(value);
						},
						"error":function(status,message){
							$scope.money_fee.outmoney_fee = 0;
						}
					})
				}else if(value == 1){
					CapitalService.system_config({
						"type":"pay-handling-amount",
						"success":function(value){
							$scope.money_fee.outmoney_fee = parseFloat(value);
						},
						"error":function(status,message){
							$scope.money_fee.outmoney_fee = 0;
						}
					})
				}
			},
			"error":function(status,message){
				$scope.money_fee.outmoney_fee = 0;
				$scope.money_fee.outmoney_fee_type = 0;
			}
		});
		CapitalService.system_config({
        	"type":"pay-least-amount",
			"success":function(value){
				$scope.money_fee.outmoneymin = value;
			},
			"error":function(status,message){
				$scope.money_fee.outmoneymin = 0;
			}
		});
  }
    
    $scope.go_add_bank = function(){
    	$scope.capital_withdraw_modal.hide();
    	$scope.user_info_modal.show();
    }
	//修改密码页面
	$scope.show_user_modal = function(){
		$scope.user_change_modal.show();
	}
	
	//修改个人银行资料页面
    $scope.show_user_bank_modal = function() {
    	$ionicHistory.clearHistory();
        $scope.user_info.bank = $scope.user_bank.userbankmes[0];
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
		var article_list = document.getElementsByClassName("today_list_footer");
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

    
    //修改个人银行资料
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
                    $scope.user_bank.userbankmes=$scope.bank_list.filter(function(obj){
						if(obj.code==$rootScope.user.bank||obj.name==$rootScope.user.bank){
							return obj;
						}
					});
                    $ionicLoading.show({
			            template: "修改成功"   
			        });
                    $timeout(function () {
                    $ionicLoading.hide();
                    $scope.user_info_modal.hide();
	                }, 2000);
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

	//修改用户密码
	$scope.update_user_pass = function(){
			if ($scope.change_userpass.oldpass == ""||$scope.change_userpass.newpass == ""||$scope.change_userpass.newpassangin == "") {
            $ionicLoading.show({ template: "密码不能为空。" });
            $timeout(function() {
                $ionicLoading.hide();
            }, 1000);
            return;
	        }
	        if ($scope.change_userpass.newpass != $scope.change_userpass.newpassangin) {
	            $ionicLoading.show({ template: "新密码两次输入不一致。" });
	            $timeout(function() {
	                $ionicLoading.hide();
	            }, 1000);
	            return;
	        }
	        if ($scope.change_userpass.newpass === $scope.change_userpass.oldpass) {
	            $ionicLoading.show({ template: "新旧密码必须不一致" });
	            $timeout(function() {
	                $ionicLoading.hide();
	            }, 1000);
	            return;
	        }
			UserService.user_change_pass({
				"oldpass":$scope.change_userpass.oldpass,
				"newpass":$scope.change_userpass.newpass,
				"success":function(message){
					$ionicLoading.show({
                    template: "修改成功"
	                });
	                $timeout(function () {
	                    $ionicLoading.hide();
	                    $scope.user_change_modal.hide();
	                }, 2000);
	                
				},
				"fail": function( message) {
	                $ionicLoading.show({
	                    template: message
	                });
	                $timeout(function () {
	                    $ionicLoading.hide();
	                }, 2000);
	            },
	            "error": function(status,message) {
	                $ionicLoading.show({
	                    template: message
	                });
	                $timeout(function () {
	                    $ionicLoading.hide();
	                }, 2000);
	            },
			});
	}
	
	
	//出金
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
				if(($rootScope.user.bankaccount)&&($rootScope.user.bankbranch)&&($rootScope.user.bankholder)&& ($rootScope.user.bank==$scope.bank_list[i].code||$rootScope.user.bank==$scope.bank_list[i].name)){
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
							
	                    $rootScope.user.amount -= ($scope.money_fee.outmoney_fee_type == 0?$scope.outAmount.outamount*($scope.money_fee.outmoney_fee+1):$scope.outAmount.outamount+$scope.money_fee.outmoney_fee);
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
    };
    //	资金历史隐藏
	$scope.capital_history_modal_hide = function(){
		$scope.has_more_money_order.if_has_more_money_order = false;
		$scope.moneyList = [];
		$scope.money_page_index = 0;
		$scope.capital_history_modal.hide();
	};
    //请求个人资金历史
    $scope.show_money_list = function() {
    	$scope.moneyList = [];
    	$scope.money_page_index = 0;
        $scope.load_more_money_order();
        $timeout(function () {
            $scope.has_more_money_order.if_has_more_money_order = true;
        }, 2000);
        $scope.capital_history_modal.show();
    };
    
    //上拉刷新
    $scope.refresh_moneylist_order = function(){
    	$scope.moneyList = [];
    	$scope.money_page_index = 0;
        $scope.has_more_money_order.if_has_more_money_order = true;
        $scope.load_more_money_order();
    };
    //下拉加载
	$scope.load_more_money_order = function(){
		
    	CapitalService.request_capital_list(
    		{
    			"startDate":$filter('date')(new Date(new Date().getTime() - 2592000000),'yyyy-MM-dd'),
    			"overDate":$filter('date')(new Date(new Date().getTime() + 86400000),'yyyy-MM-dd'),
    			"page":$scope.money_page_index + 1,
    			"size":10,
    			"success":function(protocol) {
    				if($scope.moneyList != protocol){
    					$scope.money_page_index = $scope.money_page_index + 1;
			            protocol.forEach(function(servicevalue){
		        			$scope.type_list.filter(function(arr){
		        				if(servicevalue.type==arr.value){
		        					$scope.moneyList.push({
				                        "_id": servicevalue._id,
				                        "remark": servicevalue.remark,
				                        "yearTime": $filter('date')(servicevalue.created,'yyyy-MM-dd'),
				                        "dayTime": $filter('date')(servicevalue.created,'HH:mm:ss'),
				                        "amount": servicevalue.amount,
				                        "user": servicevalue.user,
				                        "balance": servicevalue.balance,
				                        "type": servicevalue.type,
				                        "typename":arr.name
				                    });
		        				}
		        			});
		        		});
    				}else if($scope.moneyList == protocol){
    					$scope.moneyList = $scope.moneyList;
    				}
    				
		            if(protocol.length === 0) {
		                $scope.has_more_money_order.if_has_more_money_order = false;
		            }
		
		            $scope.$broadcast('scroll.refreshComplete');
		            $scope.$broadcast('scroll.infiniteScrollComplete');
		        }
    		}); 
    		
    };
    
    
    $scope.$on('$destroy', function() {
        if ($scope.user_info_modal) {
            $scope.user_info_modal.hide();
        }
        if ($scope.capital_history_modal) {
            $scope.capital_history_modal.hide();
        }
        if ($scope.pay_webview_modal) {
            $scope.pay_webview_modal.hide();
        }
        if ($scope.pay_qrcode_modal) {
            $scope.pay_qrcode_modal.hide();
        }
        if($scope.capital_deposit_modal) {
            $scope.capital_deposit_modal.hide();
        }
        if ($scope.capital_withdraw_modal) {
            $scope.capital_withdraw_modal.hide();
        }
        if($scope.user_change_modal) {
            $scope.user_change_modal.hide();
        }
    });
});
