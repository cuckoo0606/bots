angular.module('starter.controllers')

.controller('ProfileCtrl', function($scope, $rootScope, $ionicModal, $ionicLoading, $timeout, $sce, $ionicHistory,$filter,
            UserService, OrderService, CloseOrderService, AppConfigService, CapitalService) {
	$rootScope.updateUser()
	$rootScope.must_city = AppConfigService.must_city
	//省市列表
	$scope.province_list=AppConfigService.province_list;
	$scope.city_list=$scope.province_list[0].city_list;
	$scope.pay_channel_lists = {};
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
    $scope.pay_banklists = AppConfigService.pay_banklists;
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
    if($rootScope.user.bank!=null){
	    $scope.user_bank.userbankmes=$scope.bank_list.filter(function(obj){
			if(obj.code==$rootScope.user.bank||obj.name==$rootScope.user.bank){
				return obj;
			}
		});
    }
    $scope.judge_bank_value=false;
    $scope.is_get_pay_list=false;
    $scope.user_info = {
        "id_card": "",
        "bank": {},
        "bank_user": "",
        "bank_brand": "",
        "bank_card": "",
        "province":"",
		"city":"",
    };
	$scope.choseDate={
		"startDate":"",
		"endDate":""
	};
	$scope.outAmount={
		"outamount":100,
	};
    $scope.deposit = {
    	"type":'',
        "amount": 100,
    };
    $scope.inmoneybank={
    	'bankmes' : ''
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
    
    //银行列表默认显示
    $scope.changeuserbank = function(mes){
    	if(mes.bank_list.length > 0){
    		if($rootScope.user.bank){
    			var bankmes = $scope.bank_list.filter(function(obj){
    				if(obj.code==$rootScope.user.bank||obj.name==$rootScope.user.bank){
    					return obj;
    				}
    			});
    			var userbankmes = mes.pay_bank_list.filter(function(userbank){
    				if(userbank.bank_title == bankmes[0].name){
    					return userbank;
    				}
    			});
    			if(userbankmes.length > 0){
    				$scope.inmoneybank.bankmes = userbankmes[0];
    			}else{
    				$scope.inmoneybank.bankmes = mes.pay_bank_list[0];
    			}
    		}else{
    			$scope.inmoneybank.bankmes = mes.pay_bank_list[0];
    		}
    	}
    }
    //拿入金列表
	CapitalService.get_pay_channel({
		"client_type":$rootScope.iswecat == true ? 'wechat':'app',
		"success":function(data){
			if(data.length!=0){
				$scope.is_get_pay_list=true
				$scope.pay_channel_lists = data.map(function(value){
					if(value.payment_channel_style == 'wechat'){
						value.pay_color = 'pay_green';
						value.pay_bg = 'pay_green_bg';
						value.pay_icon = 'iconfont icon-weixin';
					}else{
						value.pay_color = 'pay_blue';
						value.pay_bg = 'pay_blue_bg';
						value.pay_icon = 'iconfont icon--19';
					};
					if(value.bank_list.length == 0){
						value.pay_height = 'pay_weixin';
					}else{
						value.pay_height = '';
					};
					if(value.bank_list.length > 0){
						value.bank_list_str = JSON.stringify(value.bank_list)
						value.pay_bank_list = $scope.pay_banklists.filter(function(mes){
							if(value.bank_list_str.indexOf(mes.bank_code)!=-1){
								return mes;
							}
						})
					};
					value.type=JSON.stringify({
						id:value._id,
						pay_type:value.payment_type
					})
					return value;
				});
				
				$scope.deposit.type = $scope.pay_channel_lists[0].type;
			}
		},
		'fail':function(message) {
			$scope.pay_channel_lists = [];
        },
		"error":function(status,message){
			$scope.pay_channel_lists = [];
		}
	});
	//入金界面
    $scope.show_deposit_modal = function() {

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
		
        $timeout(function () {
        	if($scope.pay_channel_lists){
        		$scope.changeuserbank($scope.pay_channel_lists[0]);
        	}
    		$scope.capital_deposit_modal.show();
        }, 500);

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

        var error = function(message) {
            $ionicLoading.show({
                template: message
            });
            $timeout(function () {
                $ionicLoading.hide();
            }, 2000);
        }
        if(JSON.parse($scope.deposit.type).pay_type =='swiftpass'){
	        CapitalService.pay_openid({
	        	'fee':$scope.deposit.amount,
	        	'payment_channel':JSON.parse($scope.deposit.type).id,
	        	'bank_code':$scope.inmoneybank.bankmes.bank_code,
	        	'openid':AppConfigService.wx_auth.openid,
	        	'success':function(mes){
	        		if($rootScope.iswecat == true){
						$ionicLoading.hide();
		                $scope.capital_deposit_modal.hide();
		                $scope.pay_qrcode_url = mes.data.action == 'qrcode'?AppConfigService.get_erweima_url + escape(mes.data.qrcode):AppConfigService.get_erweima_url + escape(mes.data.url);
		                $scope.pay_qrcode_modal.show();
			        }else{
		        		if(mes.data.action == 'qrcode'){
							$ionicLoading.hide();
			                $scope.capital_deposit_modal.hide();
			                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(mes.data.qrcode);
			                $scope.pay_qrcode_modal.show();
		        		}else if(mes.data.action == 'redirect'){
			                $ionicLoading.hide();
		                    $scope.capital_deposit_modal.hide();
		                    $scope.pay_webview_modal.show();
		                    $scope.pay_modal_url = $sce.trustAsResourceUrl(mes.data.url);
		        		}else{
		        			$ionicLoading.hide();
		        		}
			        }
		        },
	            "fail": fail,
	            "error": error
	        });
        }else{
	        CapitalService.payment({
	        	'fee':$scope.deposit.amount,
	        	'payment_channel':JSON.parse($scope.deposit.type).id,
	        	'bank_code':$scope.inmoneybank.bankmes.bank_code,
	        	'success':function(mes){
	        		if($rootScope.iswecat == true){
						$ionicLoading.hide();
		                $scope.capital_deposit_modal.hide();
		                $scope.pay_qrcode_url = mes.data.action == 'qrcode'?AppConfigService.get_erweima_url + escape(mes.data.qrcode):AppConfigService.get_erweima_url + escape(mes.data.url);
		                $scope.pay_qrcode_modal.show();
			        }else{
		        		if(mes.data.action == 'qrcode'){
							$ionicLoading.hide();
			                $scope.capital_deposit_modal.hide();
			                $scope.pay_qrcode_url = AppConfigService.get_erweima_url + escape(mes.data.qrcode);
			                $scope.pay_qrcode_modal.show();
		        		}else if(mes.data.action == 'redirect'){
			                $ionicLoading.hide();
		                    $scope.capital_deposit_modal.hide();
		                    $scope.pay_webview_modal.show();
		                    $scope.pay_modal_url = $sce.trustAsResourceUrl(mes.data.url);
		        		}else{
		        			$ionicLoading.hide();
		        		}
			        }
		        },
	            "fail": fail,
	            "error": error
	        });
        }
        
    }

	//出金页面
    $scope.show_withdraw_modal = function() {
        $scope.capital_withdraw_modal.show();
        $scope.money_fee.outmoney_bank_card = "";
        $scope.money_fee.outmoney_bank_card_icon = "";
        if($rootScope.user.bankaccount){
        	$scope.money_fee.outmoney_bank_card = '**** **** **** '+$rootScope.user.bankaccount.substring($rootScope.user.bankaccount.length-4);
        	$scope.money_fee.outmoney_bank = $scope.bank_list.filter(function(value){
				if(value.code == $rootScope.user.bank){
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
    	if($scope.user_bank.userbankmes.length>0){
    		$scope.user_info.bank = $scope.user_bank.userbankmes[0];
    	}else{
    		$scope.user_info.bank = $scope.bank_list[0]
    	}
        if($rootScope.user.province==""||$rootScope.user.city==""||$rootScope.user.province==null||$rootScope.user.city==null){
        	$scope.user_info.province = $scope.province_list[0]
        	$scope.user_info.city = $scope.city_list[0]
        	
        }else{
        	var a = $scope.province_list.filter(function(item){
        		if(item.name == $rootScope.user.province){
        			return item
        		}
        	})
        	$scope.user_info.province = a[0]
        	$scope.city_list = $scope.user_info.province.city_list
        	$scope.user_info.city = $rootScope.user.city
        }
        if($rootScope.user.idcard!=null&&$rootScope.user.bankbranch!=null&&$rootScope.user.bankholder!=null&&$rootScope.user.bankaccount!=null){
        	$scope.user_info.id_card = $rootScope.user.idcard;
	        $scope.user_info.bank_brand = $rootScope.user.bankbranch;
	        $scope.user_info.bank_user = $rootScope.user.bankholder;
	        $scope.user_info.bank_card = $rootScope.user.bankaccount;
        }
        $scope.user_info_modal.show();
    }
	
	$scope.change_city_list = function(){
		$scope.city_list = $scope.user_info.province.city_list
		$scope.user_info.city = $scope.city_list[0]
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
    	if($scope.user_info.bank==""||$scope.user_info.bank_brand==""||$scope.user_info.bank_user==""||$scope.user_info.bank_card==""||$scope.user_info.id_card==""||$scope.user_info.bank==null||$scope.user_info.bank_brand==null||$scope.user_info.bank_user==null||$scope.user_info.bank_card==null||$scope.user_info.id_card==null){
        	$ionicLoading.show({
	            template: "信息请填写完整"   
	        });
            $timeout(function () {
            	$ionicLoading.hide();
            }, 2000);
            
    	}else if($rootScope.must_city&&$scope.user_info.province==null||$scope.user_info.city==null||$scope.user_info.province==""||$scope.user_info.city==""){
            	$ionicLoading.show({
		            template: "请填写省市"   
		        });
	            $timeout(function () {
	            	$ionicLoading.hide();
	            }, 2000);
            }else{
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
	            "province":$scope.user_info.province.name,
	            "city":$scope.user_info.city,
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
		if($rootScope.must_city&&$rootScope.user.province==null||$rootScope.user.city==null||$rootScope.user.province==undefined||$rootScope.user.city==undefined&&$rootScope.user.province==""||$rootScope.user.city==""){
				$ionicLoading.show({
	            template: "请前往签约银行页面补全省市"
		        });
                $timeout(function() {
                    $ionicLoading.hide();
                }, 2000);
		}else if(judge_bank_value){
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
	                    $rootScope.updateUser()
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
        if($scope.pay_money_modal){
        	$scope.pay_money_modal.hide();
        }
    });
});
