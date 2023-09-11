import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DBDSComponent } from './dbds.component';

describe('DBDSComponent', () => {
  let component: DBDSComponent;
  let fixture: ComponentFixture<DBDSComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DBDSComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DBDSComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
