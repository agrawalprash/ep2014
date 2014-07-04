var app = angular.module('DemoApp', ['jigna']);

app.controller('DemoController', function($scope){
    $scope.active_view = 0;

    $scope.update_active = function(index){
        $scope.active_view = index;
    };
});
