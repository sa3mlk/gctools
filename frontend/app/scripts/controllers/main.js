'use strict';

angular.module('frontendApp')
  .controller('MainCtrl', function ($scope, $http, $filter, ngTableParams) {
	$scope.results = [];
	$scope.data = [];

	$scope.step1 = true;
	$scope.step2 = false;
	$scope.step3 = false;
	$scope.locating = false;

	$scope.find = function() {
		//var url = 'http://127.0.0.0:52052/gcfind/' + $scope.query;
		var url = 'http://10.0.3.202:52052/gcfind/' + $scope.query;
		console.log('URL:' + url);
		$scope.step1 = false;
		$scope.step2 = true;
		$http.get(url).success(function (response) {
			$scope.step2 = false;
			$scope.step3 = true;
			$scope.data = response;

			$scope.tableParams = new ngTableParams({
				page: 1,
				count: 100,
				sorting: { name: 'asc' }
			}, {
				counts: [],
				total: $scope.data.length,
		        getData: function($defer, params) {
					var orderedData = params.filter() ? $filter('filter')($scope.data, params.filter()) : $scope.data;
					$scope.results = orderedData.slice((params.page() - 1) * params.count(), params.page() * params.count());
					params.total(orderedData.length); // set total for recalc pagination
					$defer.resolve($scope.results);
        		}
			});
		});
	};

	$scope.myPosition = function() {
		$scope.locating = true;
		navigator.geolocation.getCurrentPosition(function(l) {
			$scope.locating = false;
			$scope.query = l.coords.latitude + ' ' + l.coords.longitude;
			$scope.find();
		});
	}

	$scope.reset = function() {
		$scope.query = "";
		$scope.results = [];
		$scope.data = [];
		$scope.step1 = true;
		$scope.step2 = false;
		$scope.step3 = false;
	}

});
