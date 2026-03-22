import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
export const Approutes: Routes = [
  {
    path: "",
    redirectTo: "admin",
    pathMatch: "full"
  },
  {
    path: "admin",
    loadChildren: () =>
      import("./admin/admin.module").then(m => m.AdminModule)
  },
   {
    path: "**",
    redirectTo: "/dashboard",
  },
  
];
