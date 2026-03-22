import { NgModule, Type } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { CommonModule, DatePipe } from '@angular/common';
import { DashboardComponent } from './admin/dashboard/dashboard.component';
import { ForecastComponent } from './admin/forecast/forecast.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ToastrModule } from "ngx-toastr";
import { FeatherModule } from "angular-feather";
import { allIcons } from "angular-feather/icons";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';


declare module "@angular/core" {
  interface ModuleWithProviders<T = any> {
    ngModule: Type<T>;
  }
}
@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    NgbModule,
    BrowserModule,
    ReactiveFormsModule,
    CommonModule,
    FormsModule,
    ToastrModule.forRoot(),
    FeatherModule.pick(allIcons),
  ],
  providers: [
    DatePipe
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }