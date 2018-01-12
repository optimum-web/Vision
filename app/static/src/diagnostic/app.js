import React from 'react';
import {Router, Route, IndexRoute, Link, hashHistory} from 'react-router'
import {Component} from 'react'
import {render} from 'react-dom'
import Equipment from './Components/Equipment';
import Home from './Components/Home';
import Campaign from './Components/Campaign';

import AddEquipmentForm from './AddEquipmentForm';
import ChooseTestForm from './ChooseTestForm';
import ElectricalProfileForm from './ElectricalProfileForm';
import FluidProfileForm from './FluidProfileForm';
import TestList from './TestList';

import NewTestForm from './NewTestForm';
import CreatedByForm from './CampaignForm_modules/NewUserForm';
import NewMaterialForm from './NewTestForm_modules/NewMaterialForm';
import NewContractForm from './CampaignForm_modules/NewContractForm';
import NewLabForm from './CampaignForm_modules/NewLabForm';
import NewFluidForm from './NewTestForm_modules/NewFluidForm';
import NewRecommendationForm from './NewTestForm_modules/NewRecommendationForm';
import TestResultForm from './TestResultForm';

import NewManufacturerForm from './EquipmentForm_modules/NewManufacturerForm';
import NewLocationForm from './EquipmentForm_modules/NewLocationForm';
import NewNormForm from './EquipmentForm_modules/NewNormForm';
import NewEquipmentTypeForm from './EquipmentForm_modules/NewEquipmentTypeForm';

import NewBushingTestForm from './TestTypeResultForm_modules/NewBushingTestForm';
import NewFuranTestForm from './TestTypeResultForm_modules/NewFuranTestForm';
import NewFluidTestForm from './TestTypeResultForm_modules/NewFluidTestForm';
import NewDissolvedGasTestForm from './TestTypeResultForm_modules/NewDissolvedGasTestForm';
import NewInhibitorTestForm from './TestTypeResultForm_modules/NewInhibitorTestForm';
import NewInsulationResistanceTestForm from './TestTypeResultForm_modules/NewInsulationResistanceTestForm';
import NewMetalsInOilTestForm from './TestTypeResultForm_modules/MetalsInOilTestForm';
import NewParticleTestForm from './TestTypeResultForm_modules/NewParticleTestForm';
import NewPcbTestForm from './TestTypeResultForm_modules/NewPcbTestForm';
import PolymerisationDegreeTestForm from './TestTypeResultForm_modules/PolymerisationDegreeTestForm';
import NewTransformerTestForm from './TestTypeResultForm_modules/NewTransformerTestForm';
import NewWindingResistanceTestForm from './TestTypeResultForm_modules/NewWindingResistanceTestForm';
import VisualTestForm from './TestTypeResultForm_modules/VisualTestForm';
import WaterTestForm from './TestTypeResultForm_modules/WaterTestForm';
import WindingTestForm from './TestTypeResultForm_modules/WindingTestForm';
import EqConnectionsManager from './EqConnectionsManager';
import NewTaskForm from './NewTaskForm';
import TaskList from './TaskList';
import GraphDetails from './GraphDetails';
import ItemDetails from './ItemDetails';
import EquipmentReport from './EquipmentReport';
import EquipmentResults from './EquipmentResults';
import UserInvite from './UserInvite';
import {NotificationContainer, NotificationManager} from 'react-notifications';


function getAPIToken() {
    return btoa(localStorage.getItem("apiToken") + ":");
}

(function ($) {
	$.authorizedAjax = function (settings) {
		var originalBeforeSendFunction = settings.beforeSend;
		settings.beforeSend = function (xhr, settings) {
			if (originalBeforeSendFunction) {
				originalBeforeSendFunction(xhr, settings);
			}
			xhr.setRequestHeader("Authorization", "Basic " + getAPIToken());
		};
		settings.statusCode = {
			401: function () {
				// Redirect user to login - ?
				NotificationManager.error("Please re-login");
			}
		};
		return $.ajax(settings);
	};
})(jQuery);

(function ($) {
    $.authorizedGet = function (url, callback, type) {
        if (type == undefined) {
            type = 'json';
        }
        return $.ajax({
            type: "GET",
            url: url,
            dataType: type,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Basic " + getAPIToken());
            },
            statusCode: {
                401: function () {
                    // Redirect user to login - ?
                    NotificationManager.error("Please re-login");
                }
            },
            success: callback
        });
    };
})(jQuery);

(function ($) {
    $.authorizedPost = function (url, callback, type) {
        if (type == undefined) {
            type = 'json';
        }
        return $.ajax({
            type: "POST",
            url: url,
            dataType: type,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", "Basic " + getAPIToken());
            },
            statusCode: {
                401: function () {
                    // Redirect user to login - ?
                    NotificationManager.error("Please re-login");
                }
            },
            success: callback
        });
    };
})(jQuery);


var LinkList = React.createClass({
    render() {
        return (
            <div className="row">
                <ul className="pull-left">
                    <li><Link to='/home'>Home</Link></li>
                    <li><Link to='/campaign'>New Campaign</Link></li>
                    <li><Link to='/equipment'>Equipment</Link></li>
                    <li><Link to='/add_equipment'>Add Equipment</Link></li>
                    <li><Link to='/campaign/1'>Campaign tests</Link></li>

                </ul>
                <ul className="pull-left">
                    <li><Link to='/add_test'>New Test</Link></li>
                    <li><Link to='/edit_test/1'>Edit Test</Link></li>
                    <li><Link to='/electro'>Electrical Profile</Link></li>
                    <li><Link to='/fluid'>Fluid Profile</Link></li>
                    <li><Link to='/choose_profile'>Choose Test Profile</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/add_createdby'>created by</Link></li>
                    <li><Link to='/add_contract'>contract</Link></li>
                    <li><Link to='/add_lab'>lab</Link></li>
                    <li><Link to='/add_material'>material</Link></li>
                    <li><Link to='/add_fluid'>new fluid</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/add_recommend'>recommend</Link></li>
                    <li><Link to='/eq_type_add'>new eq type</Link></li>
                    <li><Link to='/eq_add_manufac'>new eq manufac</Link></li>
                    <li><Link to='/eq_add_location'>new eq location</Link></li>
                    <li><Link to='/eq_add_norm'>new eq norms</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/bushing_test'>bushing test</Link></li>
                    <li><Link to='/furan_test'>furan test</Link></li>
                    <li><Link to='/fluid_test'>fluid test</Link></li>
                    <li><Link to='/dissolved_test'>dissolved gas test</Link></li>
                    <li><Link to='/inhibit_test'>inhibitor gas test</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/insulation_test'>insulation test</Link></li>
                    <li><Link to='/me_oil__test'>metals on oil test</Link></li>
                    <li><Link to='/particle_test'>particles test</Link></li>
                    <li><Link to='/pcb_test'>pcb test</Link></li>
                    <li><Link to='/polymer_test'>polymer test</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/transformer_test'>transformer test</Link></li>
                    <li><Link to='/winding_test'>winding test</Link></li>
                    <li><Link to='/visual_test'>visual test</Link></li>
                    <li><Link to='/water_test'>water test</Link></li>
                    <li><Link to='/winding2_test'>winding test2</Link></li>
                </ul>
                <ul className="pull-left">
                    <li><Link to='/up_down_streams'>Stream manager</Link></li>
                    <li><Link to='/schedule_task'>Schedule a task</Link></li>
                    <li><Link to='/tasks'>Tasks</Link></li>
                </ul>
            </div>

        )
    }
});


const App = React.createClass({
    getInitialState: function () {
        return {
            release_version: '',
        };
    },
    componentDidMount: function() {
        var url = '/api/v1.0/release_version/';
        this.serverRequest = $.authorizedGet(url,
            function (result) {

                var release_version = result['result'];
                this.setState({
                    release_version: release_version,
                });
            }.bind(this), 'json');
    },

    render() {
        var version = this.state.release_version;
        return (
            // <div className="content">
            //     <NotificationContainer/>
            //       <LinkList/>
            //     <div className='app-container'>
            //         <hr/>
            //         {this.props.children}
            //     </div>
            // </div>

            <div className="content ">
                <span className="no_print">Release version: {version}</span>
                <NotificationContainer/>
                <div className='app-container'>
                    <hr/>
                    {this.props.children}
                </div>
            </div>

        )
    }
});

render((
    <Router history={hashHistory}>
        <Route path="/" component={App}>
            <IndexRoute component={Home}/>
            <Route path="campaign" component={Campaign}/>
            <Route path="equipment" component={Equipment}/>
            <Route path="add_equipment/:campaign" component={AddEquipmentForm}/>
            <Route path="campaign/:campaign" component={TestList}/>
            <Route path="electro" component={ElectricalProfileForm}/>
            <Route path="fluid" component={FluidProfileForm}/>
            <Route path="choose_profile" component={ChooseTestForm}/>
            <Route path="add_test" component={NewTestForm}/>
            <Route path="edit_test/:id" component={NewTestForm}/>
            <Route path="add_createdby" component={CreatedByForm}/>
            <Route path="add_contract" component={NewContractForm}/>
            <Route path="add_lab" component={NewLabForm}/>
            <Route path="add_material" component={NewMaterialForm}/>
            <Route path="add_fluid" component={NewFluidForm}/>
            <Route path="add_recommend" component={NewRecommendationForm}/>
            <Route path="test_result" component={TestResultForm}/>
            <Route path="eq_type_add" component={NewEquipmentTypeForm}/>
            <Route path="eq_add_manufac" component={NewManufacturerForm}/>
            <Route path="eq_add_location" component={NewLocationForm}/>
            <Route path="eq_add_norm" component={NewNormForm}/>
            <Route path="bushing_test" component={NewBushingTestForm}/>
            <Route path="furan_test" component={NewFuranTestForm}/>
            <Route path="fluid_test" component={NewFluidTestForm}/>
            <Route path="dissolved_test" component={NewDissolvedGasTestForm}/>
            <Route path="inhibit_test" component={NewInhibitorTestForm}/>
            <Route path="insulation_test" component={NewInsulationResistanceTestForm}/>
            <Route path="me_oil__test" component={NewMetalsInOilTestForm}/>
            <Route path="particle_test" component={NewParticleTestForm}/>
            <Route path="pcb_test" component={NewPcbTestForm}/>
            <Route path="polymer_test" component={PolymerisationDegreeTestForm}/>
            <Route path="transformer_test" component={NewTransformerTestForm}/>
            <Route path="winding_test" component={NewWindingResistanceTestForm}/>
            <Route path="visual_test" component={VisualTestForm}/>
            <Route path="water_test" component={WaterTestForm}/>
            <Route path="winding2_test" component={WindingTestForm}/>
            <Route path="up_down_streams" component={EqConnectionsManager}/>
            <Route path="schedule_task" component={NewTaskForm}/>
            <Route path="tasks" component={TaskList}/>
            <Route path="graph_details/:equipmentId/:date" component={GraphDetails}/>
            <Route path="equipment_report/:equipmentId" component={EquipmentReport}/>
            <Route path="equipment_results/:equipmentId" component={EquipmentResults}/>
            <Route path="users/invite/" component={UserInvite}/>
            
            {/*This route should be the last, otherwise it will match all subsequent routes*/}
            <Route path=":equipmentId" component={Home}/>
        </Route>
    </Router>
), document.getElementById('app'));

