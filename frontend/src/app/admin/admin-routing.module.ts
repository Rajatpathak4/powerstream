import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './dashboard/dashboard.component';
import { ForecastComponent } from './forecast/forecast.component';

const routes: Routes = [
  { path: 'dashboard', 
    component: DashboardComponent 
  },
  { path: 'forecast', 
    component: ForecastComponent 
  },
  { path: '', 
    redirectTo: 'dashboard', 
    pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminRoutingModule {}