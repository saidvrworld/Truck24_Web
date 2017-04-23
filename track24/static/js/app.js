(function() {
	var app = angular.module('Track24', [ ]);
	app.controller('TrackController', function($scope, $http){
		//$http.get('http://94.158.58.98/track24/?api=test', 'api = test').then(function(response){
			//$scope.test = response.data;
		//});

		var phoneNumber = "";
		function sendData($scope){
		$http({
		    method: 'POST',
		    url: 'http://track24.beetechno.uz/api/',
		    data: phoneNumber,
		    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).then(function(response){
			$scope.test = response.data;
		});
	}
	});
})();