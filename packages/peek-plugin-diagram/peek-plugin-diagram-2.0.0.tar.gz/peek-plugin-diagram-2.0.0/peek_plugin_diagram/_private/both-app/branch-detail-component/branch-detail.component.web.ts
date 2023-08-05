import {
    ChangeDetectionStrategy,
    ChangeDetectorRef,
    Component,
    Input,
    OnInit
} from "@angular/core";
import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";
import {BranchDetailTuple, BranchService} from "@peek/peek_plugin_branch";

import {BranchTuple} from "@peek/peek_plugin_diagram/_private/branch/BranchTuple";

import {DocDbService, DocumentResultI} from "@peek/peek_plugin_docdb";
import {DispFactory} from "../canvas-shapes/DispFactory";
import {PrivateDiagramPositionService} from "@peek/peek_plugin_diagram/_private/services/PrivateDiagramPositionService";
import {DiagramPositionService} from "@peek/peek_plugin_diagram/DiagramPositionService";
import {PrivateDiagramBranchContext} from "@peek/peek_plugin_diagram/_private/branch/PrivateDiagramBranchContext";
import {PrivateDiagramBranchService} from "@peek/peek_plugin_diagram/_private/branch/PrivateDiagramBranchService";
import {assert} from "../DiagramUtil";
import {Observable} from "rxjs";
import {DispBase} from "../canvas-shapes/DispBase";


@Component({
    selector: 'pl-diagram-branch-detail',
    templateUrl: 'branch-detail.component.web.html',
    styleUrls: ['branch-detail.component.web.scss'],
    moduleId: module.id,
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class BranchDetailComponent extends ComponentLifecycleEventEmitter
    implements OnInit {

    @Input("modelSetKey")
    modelSetKey: string;

    @Input("coordSetKey")
    coordSetKey: string;

    // Set in VIEW mode from select-branches
    @Input("globalBranch")
    inputGlobalBranch: BranchDetailTuple;

    // Set in EDIT mode from edit-props
    @Input("globalBranchKey")
    globalBranchKey: string;

    globalBranch: BranchDetailTuple;

    // Set in EDIT mode from edit-props
    @Input("diagramBranchTuple")
    diagramBranch: BranchTuple;

    // Set in EDIT mode from edit-props
    @Input("diagramBranchUpdatedObservable")
    diagramBranchUpdatedObservable: Observable<void>;

    isEditMode: boolean = false;

    DETAILS_TAB = 1;
    ANCHORS_TAB = 2;
    EDITED_ITEMS_TAB = 3;
    barIndex: number = 1;

    anchorDocs: any[] = [];

    disps: any[] = [];

    private diagramPosService: PrivateDiagramPositionService;

    constructor(private cd: ChangeDetectorRef,
                private docDbService: DocDbService,
                diagramPosService: DiagramPositionService,
                private branchService: PrivateDiagramBranchService,
                private globalBranchService: BranchService) {
        super();

        this.diagramPosService = <PrivateDiagramPositionService>diagramPosService;

    }

    ngOnInit() {
        if (this.inputGlobalBranch != null) {
            this.globalBranch = this.inputGlobalBranch;
            this.globalBranchKey = this.inputGlobalBranch.key;
            this.loadDiagramBranch();
            return;
        }

        assert(this.diagramBranch != null, "diagramBranch is not set");
        assert(this.globalBranchKey != null, "globalBranchKey is not set");

        this.isEditMode = true;
        this.loadGlobalBranch();
        this.loadDiagramBranchDisps();
        this.loadDiagramBranchAnchorKeys();

        if (this.diagramBranchUpdatedObservable != null) {
            this.diagramBranchUpdatedObservable
                .takeUntil(this.onDestroyEvent)
                .subscribe(() => {
                    this.loadDiagramBranchDisps();
                    this.loadDiagramBranchAnchorKeys();
                });
        }
    }

    private loadGlobalBranch() {
        this.globalBranch = new BranchDetailTuple();

        this.globalBranchService
            .getBranch(this.modelSetKey, this.globalBranchKey)
            .then((globalBranch: BranchDetailTuple | null) => {
                if (globalBranch == null) {
                    console.log(`ERROR: Could not load global branch for ${this.globalBranchKey}`);
                    return;
                }
                this.globalBranch = globalBranch;
            })

    }

    private loadDiagramBranch() {
        this.diagramBranch = new BranchTuple();
        this.disps = [];

        this.branchService
            .getBranch(this.modelSetKey, this.coordSetKey, this.globalBranchKey)
            .then((diagramBranch: PrivateDiagramBranchContext) => {
                this.diagramBranch = diagramBranch.branchTuple;
                this.loadDiagramBranchDisps();
                this.loadDiagramBranchAnchorKeys();
                this.cd.detectChanges();
            });
    }

    private loadDiagramBranchDisps() {
        this.disps = this.diagramBranch.disps.filter(d => DispBase.groupId(d) == null);
        this.cd.detectChanges();
    }

    private loadDiagramBranchAnchorKeys() {
        let anchorKeys = this.diagramBranch.anchorDispKeys;
        if (anchorKeys == null || anchorKeys.length == 0)
            return;

        this.docDbService
            .getObjects(this.modelSetKey, anchorKeys)
            .then((docs: DocumentResultI) => {
                this.anchorDocs = [];

                for (let anchorDispKey of anchorKeys) {
                    let doc = docs[anchorDispKey];
                    let props = [{title: "Key", value: anchorDispKey}];
                    if (doc != null) {
                        props.add(this.docDbService.getNiceOrderedProperties(doc))
                    }
                    this.anchorDocs.push(props);
                }
                this.cd.detectChanges();
            });
    }

    noAnchors(): boolean {
        return this.anchorDocs.length == 0;
    }

    noDisps(): boolean {
        return this.disps.length == 0;
    }

    dispDesc(disp): string[] {
        return (DispFactory.wrapper(disp).makeShapeStr(disp)).split('\n');
    }

    positonAnchorOnDiagram(props: any[]): void {
        this.diagramPosService.positionByKey(this.modelSetKey,
            this.coordSetKey,
            {highlightKey: props[0].value});
    }

    positonDispOnDiagram(disp: any): void {
        let Wrapper = DispFactory.wrapper(disp);
        let center = Wrapper.center(disp);

        this.diagramPosService.position(
            this.coordSetKey, center.x, center.y, 5.0, Wrapper.key(disp)
        );
    }

}
