import {addTupleType, Tuple} from "@synerty/vortexjs";
import {docDbGenericMenuTuplePrefix} from "../PluginNames";


@addTupleType
export class DocDbGenericMenuTuple extends Tuple {
    public static readonly tupleName = docDbGenericMenuTuplePrefix + "DocDbGenericMenuTuple";

    //  Description of date1
    id : number;

    modelSetKey : string | null;
    coordSetKey : string | null;
    faIcon : string | null;
    title : string;
    url : string;

    constructor() {
        super(DocDbGenericMenuTuple.tupleName)
    }
}