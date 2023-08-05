import {Injectable} from "@angular/core";

import {
    DocDbPopupContextI,
    DocDbPopupService,
    DocDbPopupTypeE
} from "@peek/peek_plugin_docdb";
import {PrivateGenericTupleService} from "./PrivateGenericTupleService";
import {DocDbGenericMenuTuple} from "../tuples/DocDbGenericMenuTuple";
import {ComponentLifecycleEventEmitter, TupleSelector} from "@synerty/vortexjs";

/** DMS Object Item Popup Service
 *
 * This service allows other plugins to add information to the item select popups.
 *
 * This is a helper service to simplify integrations with the object.
 *
 */
@Injectable()
export class PrivateGenericMenuService extends ComponentLifecycleEventEmitter {

    private menus: DocDbGenericMenuTuple [] = [];

    constructor(private objectPopupService: DocDbPopupService,
                private tupleService: PrivateGenericTupleService) {
        super();

        this.tupleService.tupleDataOfflineObserver
            .subscribeToTupleSelector(new TupleSelector(DocDbGenericMenuTuple.tupleName, {}))
            .subscribe((tuples: DocDbGenericMenuTuple[]) => this.menus = tuples);

        this.objectPopupService
            .popupObservable(DocDbPopupTypeE.summaryPopup)
            .takeUntil(this.onDestroyEvent)
            .subscribe((c: DocDbPopupContextI) => this.handlePopup(c));

        this.objectPopupService
            .popupObservable(DocDbPopupTypeE.detailPopup)
            .takeUntil(this.onDestroyEvent)
            .subscribe((c: DocDbPopupContextI) => this.handlePopup(c));

    }


    private handlePopup(context: DocDbPopupContextI): void {
        if (context.key == null)
            return;

        const doc = context.document == null ? null : context.document.document;

        for (const menu of this.menus) {
            if (!(context.modelSetKey == menu.modelSetKey || menu.modelSetKey == null))
                continue;

            let url = menu.url.toLowerCase();
            url = url.replace("{key}", context.key);

            const keys = Object.keys(doc);
            for (let key of keys) {
                let val = doc[key] == null ? '' : doc[key];
                key = key.toLowerCase();
                url = url.replace(`{${key}}`, val);
            }

            context.addAction({
                name: menu.title,
                tooltip: null,
                icon: menu.faIcon,
                callback: () => this.menuClicked(menu, url),
                children: [],
                closeOnCallback: true
            });
        }
    }

    private menuClicked(menu: DocDbGenericMenuTuple, url: string): void {
        window.open(url);
    }

}