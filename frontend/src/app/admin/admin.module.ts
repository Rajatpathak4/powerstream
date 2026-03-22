import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as HC_exporting from 'highcharts/modules/exporting';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ForecastComponent } from './forecast/forecast.component';
import * as Highcharts from 'highcharts';
import { AdminRoutingModule } from './admin-routing.module';

// HC_exporting(Highcharts);


@NgModule({
  declarations: [
    DashboardComponent,
    ForecastComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
  ]
})
export class AdminModule { }


