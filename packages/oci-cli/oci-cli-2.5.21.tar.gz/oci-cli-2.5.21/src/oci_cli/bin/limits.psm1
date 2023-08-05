function GetOciTopLevelCommand_limits() {
    return 'limits'
}

function GetOciSubcommands_limits() {
    $ociSubcommands = @{
        'limits' = 'quota'
        'limits quota' = 'create delete get list update'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_limits() {
    $ociCommandsToLongParams = @{
        'limits quota create' = 'compartment-id defined-tags description freeform-tags from-json help max-wait-seconds name statements wait-for-state wait-interval-seconds'
        'limits quota delete' = 'force from-json help if-match max-wait-seconds quota-id wait-for-state wait-interval-seconds'
        'limits quota get' = 'from-json help quota-id'
        'limits quota list' = 'all compartment-id from-json help lifecycle-state limit name page page-size sort-by sort-order'
        'limits quota update' = 'defined-tags description force freeform-tags from-json help if-match max-wait-seconds quota-id statements wait-for-state wait-interval-seconds'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_limits() {
    $ociCommandsToShortParams = @{
        'limits quota create' = '? c h'
        'limits quota delete' = '? h'
        'limits quota get' = '? h'
        'limits quota list' = '? c h'
        'limits quota update' = '? h'
    }
    return $ociCommandsToShortParams
}