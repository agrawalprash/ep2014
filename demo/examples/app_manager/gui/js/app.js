var app = angular.module('AppManager', ['jigna']);

app.controller('MainCtrl', function($scope){
    $scope.view = {
        current_mode: 'dashboard'
    };
});
